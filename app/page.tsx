const research = [
  {
    n: "01",
    title: "Population neuroimaging",
    text: "Reproducible AI-assisted pipelines for diffusion MRI and imaging-derived phenotypes at biobank scale.",
  },
  {
    n: "02",
    title: "Multimodal medical AI",
    text: "Interpretable models that bring together imaging, cognition, plasma biomarkers, genomics and transcriptomics.",
  },
  {
    n: "03",
    title: "Brain disease biomarkers",
    text: "Quantitative phenotyping and patient-level prediction for Alzheimer's, Parkinson's and related disorders.",
  },
];

const publications = [
  {
    year: "2026",
    title: "Deep learning enhanced ALPS reveals genetic and environmental factors of brain glymphatic function",
    authors: "Lin, C.#, Wu, H.#, Xian, W., et al.",
    journal: "EBioMedicine, 124, 106133",
  },
  {
    year: "2025",
    title: "Impact of Y chromosome loss on the risk of Parkinson's disease and progression",
    authors: "Wang, J., Chen, X., Du, W., Lin, C., et al.",
    journal: "EBioMedicine, 117, 105769",
  },
  {
    year: "2023",
    title: "Early diagnosis of mild cognitive impairment due to Alzheimer's disease using a composite of MemTrax and blood biomarkers",
    authors: "Chen, W.#, Lin, C.#, Su, F., et al.",
    journal: "Journal of Alzheimer's Disease, 94(3), 1093–1103",
  },
  {
    year: "2022",
    title: "Inhibition of ALG3 stimulates cancer cell immunogenic ferroptosis to potentiate immunotherapy",
    authors: "Liu, P., Lin, C., et al.",
    journal: "Cellular and Molecular Life Sciences, 79(7), 352",
  },
  {
    year: "2021",
    title: "A calcium-related immune signature in prognosis prediction of patients with glioma",
    authors: "Lin, C., Chen, J., Su, Z., et al.",
    journal: "Frontiers in Cell and Developmental Biology, 9, 723103",
  },
];

const education = [
  ["2022–2026", "Ph.D. in Bioinformatics", "Zhongshan School of Medicine, Sun Yat-sen University · Shenzhen"],
  ["2019–2022", "M.S. in Cell Biology", "Zhongshan School of Medicine, Sun Yat-sen University · Guangzhou"],
  ["2015–2019", "B.S. in Bioengineering", "School of Life Sciences, South China Normal University · Guangzhou"],
];

const photos = [
  ["01", "Places I go", "For landscapes, streets and small discoveries."],
  ["02", "Things I notice", "For books, exhibitions and everyday details."],
  ["03", "Life in between", "For good food, friends and unhurried moments."],
];

export default function Home() {
  return (
    <main id="top">
      <header className="site-header">
        <nav className="nav" aria-label="Primary navigation">
          <a className="brand" href="#top">Cha Lin</a>
          <div className="nav-links">
            <a href="#research">Research</a>
            <a href="#publications">Publications</a>
            <a href="#about">About</a>
            <a href="#life">Life</a>
          </div>
          <a className="contact-link" href="mailto:linch58@mail2.sysu.edu.cn">Email me</a>
        </nav>
      </header>

      <section className="hero wrap">
        <div className="hero-main">
          <p className="overline">Computational biomedical imaging · Medical AI</p>
          <h1>Making medical images<br />more meaningful.</h1>
          <p className="intro">
            I'm <span>Cha Lin</span>, a bioinformatics researcher working at the intersection of
            neuroimaging, multimodal biomarkers and trustworthy machine learning.
          </p>
          <div className="hero-links">
            <a href="#research">Read about my work <span>↓</span></a>
            <a href="/cv/Cha_Lin_CV.pdf" target="_blank">Curriculum vitae <span>↗</span></a>
          </div>
        </div>
        <aside className="portrait-block" aria-label="Portrait of Cha Lin">
          <div className="portrait-placeholder portrait-photo">
            <img src="/profile.jpg" alt="Cha Lin" />
          </div>
          <p className="portrait-caption">Based in Shenzhen, China<br />Available to start immediately</p>
        </aside>
      </section>

      <div className="quiet-strip">
        <div className="wrap strip-inner">
          <span>Diffusion MRI</span><i />
          <span>Multimodal learning</span><i />
          <span>Clinical biomarkers</span><i />
          <span>Reproducible science</span>
        </div>
      </div>

      <section className="section wrap" id="research">
        <div className="section-intro">
          <p className="section-label">Selected research</p>
          <div>
            <h2>Questions I care about</h2>
            <p>How can imaging AI be useful beyond a single dataset? My work combines careful methodology with large cohorts and clinically grounded questions.</p>
          </div>
        </div>
        <div className="research-list">
          {research.map((item) => (
            <article key={item.n}>
              <span>{item.n}</span>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
        <div className="methods">
          <p>Methods & tools</p>
          <span>Python</span><span>R</span><span>MATLAB</span><span>FSL</span><span>SPM</span><span>FreeSurfer</span><span>MRtrix3</span><span>CONN</span>
        </div>
      </section>

      <section className="section publication-section" id="publications">
        <div className="wrap">
          <div className="section-intro compact">
            <p className="section-label">Publications</p>
            <div>
              <h2>Selected writing</h2>
              <a className="text-link" href="https://scholar.google.com/citations?user=BawOb5AAAAAJ&hl=en" target="_blank" rel="noreferrer">Complete list on Google Scholar ↗</a>
            </div>
          </div>
          <div className="papers">
            {publications.map((paper) => (
              <article className="paper" key={paper.title}>
                <p className="paper-year">{paper.year}</p>
                <div>
                  <h3>{paper.title}</h3>
                  <p>{paper.authors}</p>
                  <p className="journal">{paper.journal}</p>
                </div>
              </article>
            ))}
          </div>
          <p className="footnote"># Equal contribution</p>
        </div>
      </section>

      <section className="section wrap" id="about">
        <div className="section-intro">
          <p className="section-label">Background</p>
          <div>
            <h2>A path through biology,<br />data and medicine</h2>
            <p>My training began in bioengineering and cell biology before moving toward bioinformatics and computational imaging.</p>
          </div>
        </div>
        <div className="education">
          {education.map(([year, degree, place]) => (
            <article key={degree}>
              <p>{year}</p>
              <h3>{degree}</h3>
              <span>{place}</span>
            </article>
          ))}
        </div>
        <div className="recognition">
          <p className="section-label">Recognition</p>
          <ul>
            <li><span>2022–2026</span> First-class Doctoral Fellowship, Sun Yat-sen University</li>
            <li><span>2022</span> Outstanding Graduate, Sun Yat-sen University</li>
            <li><span>2021</span> National Scholarship, P.R. China</li>
          </ul>
        </div>
      </section>

      <section className="section life-section" id="life">
        <div className="wrap">
          <div className="life-heading">
            <p className="section-label">Outside the lab</p>
            <h2>A small archive<br />of ordinary days.</h2>
            <p>Science is only part of the picture. This space is reserved for the places, people and quiet interests that shape the rest of my life.</p>
          </div>
          <div className="photo-grid">
            {photos.map(([number, title, description]) => (
              <article className="photo-card" key={number}>
                <div className="photo-space"><span>{number}</span><p>your photo</p></div>
                <h3>{title}</h3>
                <p>{description}</p>
              </article>
            ))}
          </div>
          <p className="upload-note">Photos can be added gradually — the layout will grow with your collection.</p>
        </div>
      </section>

      <footer>
        <div className="wrap footer-main">
          <div>
            <p className="section-label">Get in touch</p>
            <h2>Let's talk about<br />images, data or ideas.</h2>
          </div>
          <div className="footer-contact">
            <a href="mailto:linch58@mail2.sysu.edu.cn">linch58@mail2.sysu.edu.cn ↗</a>
            <a href="https://scholar.google.com/citations?user=BawOb5AAAAAJ&hl=en">Google Scholar ↗</a>
            <a href="https://orcid.org/0000-0001-6376-3302">ORCID ↗</a>
          </div>
        </div>
        <div className="wrap footer-bottom"><p>© 2026 Cha Lin</p><a href="#top">Back to top ↑</a></div>
      </footer>
    </main>
  );
}
