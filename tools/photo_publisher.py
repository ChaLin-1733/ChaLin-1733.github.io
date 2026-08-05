from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import uuid
import webbrowser
from datetime import date, datetime
from pathlib import Path
from tkinter import BooleanVar, StringVar, Text, Tk, filedialog, messagebox
from tkinter import ttk

from PIL import Image, ImageOps, ImageTk


SITE_URL = "https://chalin-1733.github.io/#life"
BACKGROUND = "#f7f5ef"
CARD = "#fffdf9"
INK = "#29312c"
MUTED = "#72776f"
SAGE = "#69796d"
ROSE = "#a97872"
LINE = "#d9d8cf"
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def repo_root() -> Path:
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent)
    candidates.extend(
        [
            Path(__file__).resolve().parents[1],
            Path.home() / "Documents" / "personal website",
        ]
    )
    for candidate in candidates:
        if (candidate / ".git").exists() and (candidate / "public" / "photos" / "photos.json").exists():
            return candidate
    raise RuntimeError("找不到网站文件夹，请把工具放回 personal website 文件夹后再打开。")


def run_git(root: Path, *args: str) -> str:
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=flags,
    )
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "Git 操作失败"
        raise RuntimeError(detail)
    return result.stdout.strip()


def make_web_photo(source: Path, destination: Path) -> None:
    if source.suffix.lower() not in SUPPORTED:
        raise ValueError("目前支持 JPG、PNG 和 WebP。HEIC 照片请先在手机中导出为 JPG。")
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        image.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
        if image.mode in ("RGBA", "LA"):
            background = Image.new("RGB", image.size, "white")
            alpha = image.getchannel("A")
            background.paste(image.convert("RGB"), mask=alpha)
            image = background
        elif image.mode != "RGB":
            image = image.convert("RGB")
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, "WEBP", quality=86, method=6)


class PublisherApp:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Cha Lin · Photo Publisher")
        self.root.geometry("780x690")
        self.root.minsize(720, 650)
        self.root.configure(bg=BACKGROUND)
        self.root_path = repo_root()
        self.selected_photo: Path | None = None
        self.preview_image: ImageTk.PhotoImage | None = None
        self.pending_push = False

        self.title_var = StringVar()
        self.date_var = StringVar(value=date.today().isoformat())
        self.path_var = StringVar(value="还没有选择照片")
        self.status_var = StringVar(value="照片只会发布到你的个人网站。")
        self.open_after_var = BooleanVar(value=True)

        self._configure_style()
        self._build()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=BACKGROUND)
        style.configure("Card.TFrame", background=CARD, borderwidth=1, relief="solid")
        style.configure("Title.TLabel", background=BACKGROUND, foreground=INK, font=("Segoe UI Semibold", 22))
        style.configure("Subtitle.TLabel", background=BACKGROUND, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Label.TLabel", background=CARD, foreground=INK, font=("Segoe UI Semibold", 10))
        style.configure("Hint.TLabel", background=CARD, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Status.TLabel", background=BACKGROUND, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("TEntry", fieldbackground="#ffffff", bordercolor=LINE, padding=7)
        style.configure("Primary.TButton", background=SAGE, foreground="white", borderwidth=0, padding=(18, 11), font=("Segoe UI Semibold", 10))
        style.map("Primary.TButton", background=[("active", "#56685b"), ("disabled", "#aeb7b0")])
        style.configure("Secondary.TButton", background="#eeeae3", foreground=INK, borderwidth=0, padding=(13, 9))
        style.map("Secondary.TButton", background=[("active", "#e1ddd5")])
        style.configure("TCheckbutton", background=CARD, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Sage.Horizontal.TProgressbar", background=ROSE, troughcolor="#e9e5de", borderwidth=0)

    def _build(self) -> None:
        outer = ttk.Frame(self.root, padding=(34, 27, 34, 24))
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="Photo Publisher", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="选择一张照片，写下配文，然后一键发布到网站的 Life 页面。",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 20))

        card = ttk.Frame(outer, style="Card.TFrame", padding=22)
        card.pack(fill="both", expand=True)
        card.columnconfigure(1, weight=1)

        preview_frame = ttk.Frame(card, width=250, height=315, style="TFrame")
        preview_frame.grid(row=0, column=0, rowspan=9, sticky="n", padx=(0, 24))
        preview_frame.grid_propagate(False)
        self.preview = ttk.Label(
            preview_frame,
            text="PHOTO\nPREVIEW",
            anchor="center",
            justify="center",
            foreground="#8b928b",
            background="#ebe8e1",
            font=("Segoe UI", 9),
        )
        self.preview.pack(fill="both", expand=True)

        choose = ttk.Button(card, text="选择照片", style="Secondary.TButton", command=self.choose_photo)
        choose.grid(row=0, column=1, sticky="w")
        ttk.Label(card, textvariable=self.path_var, style="Hint.TLabel", wraplength=400).grid(
            row=1, column=1, sticky="ew", pady=(7, 18)
        )

        ttk.Label(card, text="小标题（可选）", style="Label.TLabel").grid(row=2, column=1, sticky="w")
        self.title_entry = ttk.Entry(card, textvariable=self.title_var)
        self.title_entry.grid(row=3, column=1, sticky="ew", pady=(6, 15))

        ttk.Label(card, text="配文", style="Label.TLabel").grid(row=4, column=1, sticky="w")
        self.caption = Text(
            card,
            height=7,
            wrap="word",
            relief="solid",
            borderwidth=1,
            highlightthickness=0,
            font=("Segoe UI", 10),
            foreground=INK,
            background="#ffffff",
            insertbackground=INK,
            padx=9,
            pady=8,
        )
        self.caption.grid(row=5, column=1, sticky="nsew", pady=(6, 15))

        meta = ttk.Frame(card, style="Card.TFrame")
        meta.grid(row=6, column=1, sticky="ew")
        ttk.Label(meta, text="日期", style="Label.TLabel").pack(side="left")
        self.date_entry = ttk.Entry(meta, textvariable=self.date_var, width=13)
        self.date_entry.pack(side="left", padx=(10, 18))
        ttk.Checkbutton(meta, text="发布成功后打开网站", variable=self.open_after_var).pack(side="left")

        ttk.Label(
            card,
            text="发布时会自动缩小照片并移除 EXIF 定位等隐私信息。",
            style="Hint.TLabel",
        ).grid(row=7, column=1, sticky="w", pady=(14, 0))

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(18, 0))
        self.progress = ttk.Progressbar(actions, mode="indeterminate", length=120, style="Sage.Horizontal.TProgressbar")
        self.progress.pack(side="left")
        ttk.Label(actions, textvariable=self.status_var, style="Status.TLabel", wraplength=390).pack(
            side="left", padx=(12, 10)
        )
        ttk.Button(actions, text="查看网站", style="Secondary.TButton", command=lambda: webbrowser.open(SITE_URL)).pack(
            side="right", padx=(8, 0)
        )
        self.publish_button = ttk.Button(actions, text="一键发布", style="Primary.TButton", command=self.publish)
        self.publish_button.pack(side="right")

    def choose_photo(self) -> None:
        selected = filedialog.askopenfilename(
            title="选择准备发布的照片",
            filetypes=[("照片", "*.jpg *.jpeg *.png *.webp"), ("所有文件", "*.*")],
        )
        if not selected:
            return
        source = Path(selected)
        try:
            with Image.open(source) as opened:
                image = ImageOps.exif_transpose(opened)
                image.thumbnail((246, 311), Image.Resampling.LANCZOS)
                preview = image.convert("RGB")
            self.preview_image = ImageTk.PhotoImage(preview)
            self.preview.configure(image=self.preview_image, text="")
            self.selected_photo = source
            self.path_var.set(source.name)
            self.status_var.set("准备好了。确认配文后即可发布。")
        except Exception as exc:
            messagebox.showerror("无法读取照片", str(exc), parent=self.root)

    def publish(self) -> None:
        if self.pending_push:
            self._start_job(self._retry_push)
            return
        if not self.selected_photo:
            messagebox.showinfo("请选择照片", "请先选择一张要发布的照片。", parent=self.root)
            return
        caption = self.caption.get("1.0", "end").strip()
        title = self.title_var.get().strip()
        if not caption and not title:
            messagebox.showinfo("请写一点内容", "小标题或配文至少填写一项。", parent=self.root)
            return
        try:
            datetime.strptime(self.date_var.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("日期格式不正确", "请使用 YYYY-MM-DD，例如 2026-08-05。", parent=self.root)
            return
        self._start_job(lambda: self._publish_job(title, caption, self.date_var.get().strip()))

    def _start_job(self, job) -> None:
        self.publish_button.configure(state="disabled")
        self.progress.start(12)
        self.status_var.set("正在处理并发布，请稍候…")
        threading.Thread(target=job, daemon=True).start()

    def _publish_job(self, title: str, caption: str, published_date: str) -> None:
        source = self.selected_photo
        if source is None:
            return
        photo_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6]
        relative_image = f"/photos/{photo_id}.webp"
        destination = self.root_path / "public" / "photos" / f"{photo_id}.webp"
        json_path = self.root_path / "public" / "photos" / "photos.json"
        original_json = json_path.read_text(encoding="utf-8")
        committed = False
        try:
            make_web_photo(source, destination)
            entries = json.loads(original_json)
            entries.insert(
                0,
                {
                    "id": photo_id,
                    "image": relative_image,
                    "title": title,
                    "caption": caption,
                    "date": published_date,
                },
            )
            temporary = json_path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporary, json_path)

            run_git(self.root_path, "add", "--", "public/photos/photos.json", f"public/photos/{destination.name}")
            run_git(self.root_path, "commit", "-m", f"Add life photo for {published_date}")
            committed = True
            self.pending_push = True
            run_git(self.root_path, "push", "origin", "main")
            self.pending_push = False
            self.root.after(0, self._publish_success)
        except Exception as exc:
            if not committed:
                try:
                    json_path.write_text(original_json, encoding="utf-8")
                    if destination.exists():
                        destination.unlink()
                    run_git(self.root_path, "restore", "--staged", "--", "public/photos/photos.json", f"public/photos/{destination.name}")
                except Exception:
                    pass
            self.root.after(0, lambda: self._publish_failed(str(exc), committed))

    def _retry_push(self) -> None:
        try:
            run_git(self.root_path, "push", "origin", "main")
            self.pending_push = False
            self.root.after(0, self._publish_success)
        except Exception as exc:
            self.root.after(0, lambda: self._publish_failed(str(exc), True))

    def _publish_success(self) -> None:
        self.progress.stop()
        self.publish_button.configure(state="normal", text="一键发布")
        self.status_var.set("发布成功。网站通常会在 1-3 分钟内更新。")
        self.selected_photo = None
        self.preview_image = None
        self.preview.configure(image="", text="PHOTO\nPREVIEW")
        self.path_var.set("还没有选择照片")
        self.title_var.set("")
        self.caption.delete("1.0", "end")
        if self.open_after_var.get():
            webbrowser.open(SITE_URL)
        messagebox.showinfo("发布成功", "照片和配文已经提交，网站通常会在 1-3 分钟内更新。", parent=self.root)

    def _publish_failed(self, detail: str, committed: bool) -> None:
        self.progress.stop()
        self.publish_button.configure(state="normal")
        if committed:
            self.pending_push = True
            self.publish_button.configure(text="重试发布")
            self.status_var.set("照片已安全保存在电脑上，但网络发布没有完成。")
        else:
            self.status_var.set("这次没有发布，原照片未受影响。")
        messagebox.showerror("发布没有完成", detail, parent=self.root)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    try:
        PublisherApp().run()
    except Exception as error:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Photo Publisher 无法启动", str(error), parent=root)
        root.destroy()
