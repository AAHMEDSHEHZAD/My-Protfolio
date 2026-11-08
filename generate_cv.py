import base64
import subprocess
import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Ahmed Shehzad - CV</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 0;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      color: #1e293b;
      background: #ffffff;
      width: 210mm;
      height: 297mm;
      max-height: 297mm;
      overflow: hidden;
      display: flex;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
    a {
      color: inherit;
      text-decoration: none;
    }

    /* Left Sidebar */
    .sidebar {
      width: 68mm;
      background: #0f172a;
      color: #f8fafc;
      padding: 18mm 6mm 14mm 8mm;
      display: flex;
      flex-direction: column;
      gap: 12px;
      border-right: 2px solid #8b5cf6;
    }
    .photo-container {
      text-align: center;
      margin-bottom: 2px;
    }
    .photo {
      width: 38mm;
      height: 38mm;
      border-radius: 50%;
      object-fit: cover;
      object-position: center top;
      border: 3px solid #a855f7;
      box-shadow: 0 4px 14px rgba(168, 85, 247, 0.4);
    }
    .side-section {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .side-title {
      font-size: 8.5pt;
      font-weight: 700;
      letter-spacing: 1.2px;
      text-transform: uppercase;
      color: #c084fc;
      border-bottom: 1px solid rgba(192, 132, 252, 0.25);
      padding-bottom: 3px;
      margin-bottom: 2px;
    }
    .contact-list {
      display: flex;
      flex-direction: column;
      gap: 5px;
      font-size: 7.6pt;
    }
    .contact-item {
      display: flex;
      align-items: flex-start;
      gap: 6px;
      color: #cbd5e1;
      word-break: break-word;
      line-height: 1.25;
    }
    .contact-item svg {
      width: 11px;
      height: 11px;
      min-width: 11px;
      margin-top: 1px;
      fill: #a855f7;
    }
    .contact-item a {
      color: #e2e8f0;
      transition: color 0.2s;
    }
    .contact-item a:hover {
      color: #c084fc;
      text-decoration: underline;
    }
    .highlight-link {
      color: #38bdf8 !important;
      font-weight: 600;
    }

    .skill-group {
      margin-bottom: 3px;
    }
    .skill-group-name {
      font-size: 7.2pt;
      font-weight: 700;
      color: #94a3b8;
      text-transform: uppercase;
      margin-bottom: 3px;
    }
    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 3.5px;
    }
    .tag {
      background: rgba(168, 85, 247, 0.16);
      color: #f1f5f9;
      font-size: 6.8pt;
      padding: 1.5px 6px;
      border-radius: 3px;
      border: 0.5px solid rgba(168, 85, 247, 0.35);
      font-weight: 500;
    }
    .tag.primary {
      background: rgba(168, 85, 247, 0.3);
      border-color: #a855f7;
      color: #ffffff;
      font-weight: 600;
    }

    .info-badge {
      font-size: 7.2pt;
      color: #cbd5e1;
      line-height: 1.35;
    }

    /* Main Content */
    .main {
      width: 142mm;
      padding: 16mm 10mm 14mm 10mm;
      display: flex;
      flex-direction: column;
      gap: 9px;
      background: #ffffff;
    }
    .header {
      border-bottom: 2px solid #f1f5f9;
      padding-bottom: 8px;
    }
    .name {
      font-size: 21pt;
      font-weight: 800;
      color: #0f172a;
      letter-spacing: -0.3px;
      line-height: 1.1;
    }
    .name span {
      color: #7c3aed;
    }
    .role-title {
      font-size: 9pt;
      font-weight: 700;
      color: #6d28d9;
      margin-top: 3px;
      letter-spacing: 0.3px;
      text-transform: uppercase;
    }
    .portfolio-pill {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      margin-top: 5px;
      background: #f5f3ff;
      border: 1px solid #ddd6fe;
      padding: 2.5px 8px;
      border-radius: 20px;
      font-size: 7.5pt;
      color: #6d28d9;
      font-weight: 600;
    }
    .portfolio-pill svg {
      width: 10px;
      height: 10px;
      fill: #6d28d9;
    }

    .section {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .section-title {
      font-size: 9.5pt;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 6px;
      border-bottom: 1.5px solid #7c3aed;
      padding-bottom: 2px;
      margin-bottom: 2px;
    }
    .section-title svg {
      width: 12px;
      height: 12px;
      fill: #7c3aed;
    }

    .summary-text {
      font-size: 7.6pt;
      color: #334155;
      line-height: 1.38;
      text-align: justify;
    }

    .timeline-item {
      margin-bottom: 4px;
    }
    .item-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }
    .item-title {
      font-size: 8.4pt;
      font-weight: 700;
      color: #0f172a;
    }
    .item-date {
      font-size: 7pt;
      font-weight: 600;
      color: #7c3aed;
      white-space: nowrap;
    }
    .item-sub {
      font-size: 7.4pt;
      font-weight: 600;
      color: #475569;
      margin-bottom: 2px;
    }
    .item-bullets {
      list-style-type: none;
      padding-left: 0;
    }
    .item-bullets li {
      position: relative;
      padding-left: 10px;
      font-size: 7.3pt;
      color: #334155;
      line-height: 1.32;
      margin-bottom: 1.5px;
    }
    .item-bullets li::before {
      content: "•";
      position: absolute;
      left: 1px;
      top: -0.5px;
      color: #7c3aed;
      font-size: 9pt;
      font-weight: bold;
    }

    .project-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .project-card {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-left: 2.5px solid #7c3aed;
      padding: 4px 6px;
      border-radius: 4px;
    }
    .proj-title {
      font-size: 7.8pt;
      font-weight: 700;
      color: #0f172a;
      display: flex;
      justify-content: space-between;
    }
    .proj-link {
      font-size: 6.8pt;
      color: #7c3aed;
      font-weight: 600;
    }
    .proj-desc {
      font-size: 6.9pt;
      color: #475569;
      line-height: 1.25;
      margin-top: 2px;
    }

    .edu-item {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }
    .edu-title {
      font-size: 8.2pt;
      font-weight: 700;
      color: #0f172a;
    }
    .edu-school {
      font-size: 7.3pt;
      font-weight: 600;
      color: #475569;
    }
    .edu-details {
      font-size: 7pt;
      color: #64748b;
      margin-top: 1px;
    }

    .awards-list {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4px;
    }
    .award-item {
      font-size: 7pt;
      color: #334155;
      line-height: 1.25;
      background: #faf5ff;
      border: 0.5px solid #e9d5ff;
      padding: 3px 6px;
      border-radius: 3px;
    }
    .award-item strong {
      color: #6b21a8;
      display: block;
      font-size: 7.2pt;
    }
  </style>
</head>
<body>

  <!-- LEFT SIDEBAR -->
  <aside class="sidebar">
    <div class="photo-container">
      <img src="data:image/jpeg;base64,{IMAGE_B64}" alt="Ahmed Shehzad" class="photo">
    </div>

    <!-- CONTACT SECTION -->
    <div class="side-section">
      <div class="side-title">Contact & Links</div>
      <div class="contact-list">
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>
          <span>Islamabad, Pakistan</span>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <a href="tel:+923189377236">+92 318 9377236</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
          <a href="mailto:as.shehzadahmed@gmail.com">as.shehzadahmed@gmail.com</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
          <a href="https://my-portfolio-gamma-ashen-6kcsqp713c.vercel.app/" target="_blank" class="highlight-link">my-portfolio-gamma-ashen.vercel.app</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
          <a href="https://www.linkedin.com/in/ahmed-shehzad-58a8a6312/" target="_blank">linkedin.com/in/ahmed-shehzad</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
          <a href="https://github.com/AAHMEDSHEHZAD" target="_blank">github.com/AAHMEDSHEHZAD</a>
        </div>
      </div>
    </div>

    <!-- TECHNICAL SKILLS -->
    <div class="side-section">
      <div class="side-title">Technical Skills</div>

      <div class="skill-group">
        <div class="skill-group-name">AI & Automation</div>
        <div class="tags">
          <span class="tag primary">N8N Automation</span>
          <span class="tag primary">AI Agents & LLMs</span>
          <span class="tag">Prompt Engineering</span>
          <span class="tag">Workflow Design</span>
          <span class="tag">Machine Learning</span>
        </div>
      </div>

      <div class="skill-group">
        <div class="skill-group-name">Development & APIs</div>
        <div class="tags">
          <span class="tag primary">Python</span>
          <span class="tag">FastAPI</span>
          <span class="tag">REST APIs</span>
          <span class="tag">JavaScript</span>
          <span class="tag">React.js</span>
          <span class="tag">HTML / CSS</span>
        </div>
      </div>

      <div class="skill-group">
        <div class="skill-group-name">Data & Databases</div>
        <div class="tags">
          <span class="tag primary">Web Scraping</span>
          <span class="tag">SQL / MySQL</span>
          <span class="tag">Data Extraction</span>
          <span class="tag">Data Analytics</span>
        </div>
      </div>

      <div class="skill-group">
        <div class="skill-group-name">Tools & Integration</div>
        <div class="tags">
          <span class="tag">Git / GitHub</span>
          <span class="tag">MS Office</span>
          <span class="tag">Workday Payroll Int.</span>
        </div>
      </div>
    </div>

    <!-- LANGUAGES & STRENGTHS -->
    <div class="side-section">
      <div class="side-title">Languages</div>
      <div class="contact-list">
        <div class="info-badge"><strong>English:</strong> Professional Proficiency</div>
        <div class="info-badge"><strong>Urdu:</strong> Native / Bilingual</div>
      </div>
    </div>

    <div class="side-section">
      <div class="side-title">Key Competencies</div>
      <div class="tags">
        <span class="tag">Complex Problem Solving</span>
        <span class="tag">System Architecture</span>
        <span class="tag">Cross-functional Teamwork</span>
        <span class="tag">Time Management</span>
      </div>
    </div>
  </aside>

  <!-- MAIN BODY -->
  <main class="main">
    <!-- HEADER -->
    <header class="header">
      <h1 class="name">Ahmed <span>Shehzad</span></h1>
      <div class="role-title">AI Engineer &bull; Python Developer &bull; Automation Specialist</div>
      <a href="https://my-portfolio-gamma-ashen-6kcsqp713c.vercel.app/" target="_blank" class="portfolio-pill">
        <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
        <span>Live Portfolio: my-portfolio-gamma-ashen-6kcsqp713c.vercel.app</span>
      </a>
    </header>

    <!-- PROFESSIONAL SUMMARY -->
    <section class="section">
      <h2 class="section-title">
        <svg viewBox="0 0 24 24"><path d="M12 2a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 8a3 3 0 1 1 3-3 3 3 0 0 1-3 3zm9 11v-1a7 7 0 0 0-7-7h-4a7 7 0 0 0-7 7v1h2v-1a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5v1z"/></svg>
        Professional Summary
      </h2>
      <p class="summary-text">
        Proactive and results-driven <strong>AI Engineer & Automation Developer</strong> with proven expertise in building intelligent systems, scalable workflow automations (n8n), and robust Python backend services. Experienced in engineering multi-step AI agents, web scraping architectures, and REST API integrations that bridge artificial intelligence with practical enterprise operations. Passionate about architectural scalability, data precision, and continuous technology innovation.
      </p>
    </section>

    <!-- WORK EXPERIENCE -->
    <section class="section">
      <h2 class="section-title">
        <svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/></svg>
        Work Experience
      </h2>

      <div class="timeline-item">
        <div class="item-header">
          <span class="item-title">Senior AI Engineer &amp; Automation Developer</span>
          <span class="item-date">Sep 2025 &ndash; Present</span>
        </div>
        <div class="item-sub">Self Employed &bull; Islamabad, Pakistan (Remote)</div>
        <ul class="item-bullets">
          <li>Architect and deploy intelligent agents and scalable automation systems using Python and modern AI platforms.</li>
          <li>Design modular n8n workflow systems utilizing Main &amp; Sub-Workflow patterns for automated CRM and lead operations.</li>
          <li>Integrate third-party RESTful APIs, LLM providers (Anthropic, OpenAI), and webhook handlers for end-to-end automation.</li>
        </ul>
      </div>

      <div class="timeline-item">
        <div class="item-header">
          <span class="item-title">Web Scraping Developer</span>
          <span class="item-date">Jun 2025 &ndash; Present</span>
        </div>
        <div class="item-sub">Linkamber &bull; Remote</div>
        <ul class="item-bullets">
          <li>Develop automated Python scraping scripts and extraction pipelines to collect and clean structured business data.</li>
          <li>Implement automated scheduling, data verification routines, and error handling for high reliability and throughput.</li>
        </ul>
      </div>

      <div class="timeline-item">
        <div class="item-header">
          <span class="item-title">Resource Person (RP)</span>
          <span class="item-date">Jul 2024 &ndash; Jul 2025</span>
        </div>
        <div class="item-sub">NRSP (National Rural Support Programme) &bull; British Council</div>
        <ul class="item-bullets">
          <li>Facilitated technical learning sessions and community youth empowerment training programs.</li>
          <li>Mentored participants in practical digital skills, teamwork execution, and structured problem solving.</li>
        </ul>
      </div>
    </section>

    <!-- FEATURED PROJECTS -->
    <section class="section">
      <h2 class="section-title">
        <svg viewBox="0 0 24 24"><path d="M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H8V4h12v12z"/></svg>
        Featured Projects
      </h2>
      <div class="project-grid">
        <div class="project-card">
          <div class="proj-title">
            <span>Email Verifier Tool</span>
            <a href="https://github.com/AAHMEDSHEHZAD/email-verifier" target="_blank" class="proj-link">GitHub &nearr;</a>
          </div>
          <p class="proj-desc">
            Python application verifying email deliverability via MX lookup, syntax validation, and SMTP checks to reduce bounce rates.
          </p>
        </div>
        <div class="project-card">
          <div class="proj-title">
            <span>n8n Intelligent Automation</span>
            <a href="https://my-portfolio-gamma-ashen-6kcsqp713c.vercel.app/" target="_blank" class="proj-link">Portfolio &nearr;</a>
          </div>
          <p class="proj-desc">
            Multi-node automated pipeline integrating AI models, CRM sync, and automated lead processing with custom error recovery.
          </p>
        </div>
      </div>
    </section>

    <!-- EDUCATION -->
    <section class="section">
      <h2 class="section-title">
        <svg viewBox="0 0 24 24"><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/></svg>
        Education
      </h2>
      <div class="edu-item">
        <div>
          <div class="edu-title">Bachelor of Science in Computer Science (BSCS)</div>
          <div class="edu-school">Abdul Wali Khan University &bull; 6th Semester (In Progress)</div>
        </div>
        <div class="item-date">Jun 2024 &ndash; Present</div>
      </div>
      <div class="edu-details">
        Focus: Algorithms, Relational Databases (SQL), Software Engineering, Web Scraping &amp; AI Fundamentals.
      </div>
    </section>

    <!-- CERTIFICATIONS & HONORS -->
    <section class="section">
      <h2 class="section-title">
        <svg viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg>
        Certifications &amp; Achievements
      </h2>
      <div class="awards-list">
        <div class="award-item">
          <strong>Student Innovation Award (Aug 2024)</strong>
          Appreciation Award at JMC Level for developing an innovative technical project.
        </div>
        <div class="award-item">
          <strong>n8n Automation &amp; GTM (Sep 2026)</strong>
          Professional Certification by Linkamber &bull; ID: crd_pOf2UbHzb.
        </div>
        <div class="award-item">
          <strong>AI Fundamentals Trainee</strong>
          HP LIFE / HP Foundation &bull; Core AI Systems &amp; Real-world Applications.
        </div>
        <div class="award-item">
          <strong>Web Development Certification</strong>
          SafeX Solutions (Jun 2026) &bull; ID: Q5$m8i#31@X%L6.
        </div>
      </div>
    </section>
  </main>

</body>
</html>
"""

def generate():
    img_path = r'd:\Portfolio\assets\profile.jpg'
    with open(img_path, 'rb') as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    rendered_html = html_template.replace('{IMAGE_B64}', img_b64)
    html_file = r'd:\Portfolio\cv.html'
    pdf_file = r'd:\Portfolio\Ahmed_Shehzad_CV.pdf'

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    print("HTML saved:", html_file)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--allow-file-access-from-files",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_file}",
        html_file
    ]
    
    print("Running Edge PDF print...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Edge return code:", res.returncode)
    if os.path.exists(pdf_file):
        print("PDF generated successfully! Size:", os.path.getsize(pdf_file), "bytes")
    else:
        print("Error: PDF not found!")

if __name__ == '__main__':
    generate()
