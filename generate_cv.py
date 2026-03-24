from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, KeepTogether


PDF_PATH = "Mohammad_Imran_Hossain_CV.pdf"


def p(text, style):
    return Paragraph(text, style)


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="Name",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1E2522"),
        spaceAfter=4,
    )
)
styles.add(
    ParagraphStyle(
        name="Role",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#1E4A3A"),
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#4B5B53"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E2522"),
        alignment=TA_LEFT,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=14,
        textColor=colors.HexColor("#1E4A3A"),
        spaceBefore=8,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="EntryTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=12.5,
        textColor=colors.HexColor("#1E2522"),
        spaceAfter=1,
    )
)
styles.add(
    ParagraphStyle(
        name="EntryMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=11.5,
        textColor=colors.HexColor("#6A7771"),
        spaceAfter=2,
    )
)


def section(title):
    return [Spacer(1, 0.16 * cm), p(title, styles["Section"])]


def entry(title, meta, bullets=None, body=None):
    items = [p(title, styles["EntryTitle"]), p(meta, styles["EntryMeta"])]
    if body:
      items.append(p(body, styles["Body"]))
    if bullets:
        for bullet in bullets:
            items.append(p(f"&bull; {bullet}", styles["Body"]))
    return KeepTogether(items + [Spacer(1, 0.07 * cm)])


doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=A4,
    topMargin=1.35 * cm,
    bottomMargin=1.2 * cm,
    leftMargin=1.45 * cm,
    rightMargin=1.45 * cm,
)

story = [
    p("Mohammad Imran Hossain", styles["Name"]),
    p("PhD Applicant in AI for Healthcare", styles["Role"]),
    p(
        "Paris Area, France | hossainimran.maia@gmail.com | github.com/imran-maia | linkedin.com/in/mohammad-imran-hossain-23721812a",
        styles["Contact"],
    ),
    p(
        "Research engineer with training across computational pathology, multimodal AI, and medical image analysis. "
        "Current work at Institut Curie focuses on integrating histopathology and spatial transcriptomics to study the tumor microenvironment. "
        "Seeking PhD positions for the 2026/2027 intake in multimodal medical AI, computational pathology, and medical image analysis.",
        styles["Body"],
    ),
]

story += section("Research Interests")
story += [
    p(
        "Computational pathology; multimodal AI for healthcare; medical image analysis; spatial transcriptomics; "
        "weakly supervised learning; self-supervised learning; segmentation; registration; image reconstruction; AI-assisted diagnosis.",
        styles["Body"],
    )
]

story += section("Research Experience")
story += [
    entry(
        "Research Engineer - Bioinformatics & AI",
        "Institut Curie - PSL Research University, Paris, France | Oct 2025 - Present",
        bullets=[
            "Developing multimodal computational pipelines integrating histopathology and spatial transcriptomics to study tumor microenvironment dynamics.",
            "Contributing to clinically grounded AI workflows for cancer biology with a focus on reproducible analysis and manuscript preparation.",
        ],
    ),
    entry(
        "Research Intern - Bioinformatics & Spatial Transcriptomics",
        "Institut Curie / Sanofi collaboration, Paris, France | Feb 2025 - Aug 2025",
        bullets=[
            "Built analysis pipelines for Visium V2 and Visium HD spatial transcriptomics data.",
            "Identified eight candidate genes potentially mediating CAF-driven T-cell exclusion in lung squamous cell carcinoma.",
            "Contributed to ongoing manuscript preparation.",
        ],
    ),
    entry(
        "Research Intern - Computational Pathology",
        "National Center for Scientific Research (CNRS), France | Feb 2024 - Jul 2024",
        bullets=[
            "Benchmarked fully supervised, weakly supervised, and self-supervised methods for homologous recombination deficiency detection in breast and ovarian cancer whole-slide images.",
            "Evaluated attention-based multiple instance learning and foundation-model-based pipelines.",
            "Best performance reached AUC 0.78 on breast cancer and 0.68 on ovarian cancer.",
        ],
    ),
    entry(
        "Visiting Researcher - Medical Image Analysis",
        "Diagnostic Image Analysis Group, Radboud University Medical Center, Netherlands | Aug 2023 - Oct 2023",
        bullets=[
            "Developed preprocessing pipelines for k-space undersampling and evaluated deep learning models for real-time MRI reconstruction in interventional radiology.",
        ],
    ),
]

story += section("Education")
story += [
    entry(
        "Master of Computer Science, Bioinformatics and Modeling",
        "Sorbonne University, France | 2024 - 2025",
        body="Grade: 14.85/20 | Rank: 1st of 8 | Best Thesis Award<br/>Thesis: Identification of Tumor Gene Signatures Underlying Fibroblast-Mediated T Cell Exclusion in Lung Cancer Using Spatial Transcriptomics.",
    ),
    entry(
        "Erasmus Mundus Joint Master's in Medical Imaging and Applications",
        "University of Girona, University of Cassino, University of Burgundy | 2022 - 2024",
        body="Grade: 8.30/10 | Fully funded by the European Union (EUR 42,000).",
    ),
    entry(
        "17th EXCITE Summer School on Biomedical Imaging",
        "ETH Zurich and University of Zurich, Switzerland | 2023",
        body="4 ECTS.",
    ),
    entry(
        "B.Sc. in Electrical and Electronic Engineering",
        "United International University, Bangladesh | 2018 - 2022",
        body="GPA: 3.97/4.00 | Summa Cum Laude | Rank: 1st of 120.",
    ),
]

story += section("Preprints and Manuscripts")
story += [
    entry(
        "Tumor Gene Signatures Underlying Fibroblast-Mediated T Cell Exclusion in Lung Cancer",
        "Institut Curie / Sanofi collaboration | In preparation",
        body="Hossain M.I. et al. Manuscript in preparation, 2026.",
    ),
    entry(
        "Comparative Study of Probabilistic Atlas and Deep Learning for Brain Tissue Segmentation",
        "ArXiv 2024",
        body="Hossain M.I., Amin M.Z., et al. arXiv:2411.05456",
    ),
    entry(
        "Deep Learning and Classical Computer Vision in Medical Image Analysis",
        "ArXiv 2025",
        body="Tweneboah A.D., Hossain M.I. (co-author), et al. arXiv:2502.19258",
    ),
]

story += section("Selected Projects")
story += [
    entry("Spatial Transcriptomics Analysis of Tumor Immune Exclusion", "Institut Curie / Sanofi | 2025", body="Visium HD pipeline for identifying CAF-mediated T-cell exclusion signatures in lung squamous cell carcinoma."),
    entry("HRD Detection in Cancer WSIs via Foundation Models and MIL", "CNRS | 2024", body="Benchmarked AB-MIL, CLAM, Trans-MIL, and foundation models for homologous recombination deficiency detection."),
    entry("Cardiac Structure Segmentation from 2D Echocardiograms", "Sorbonne University | 2025", body="nnU-Net pipeline for echocardiogram segmentation. Dice scores: LV endocardium 0.94, LV epicardium 0.91, left atrium 0.93."),
    entry("Breast Cancer Subtype Classification via Multi-omics Integration", "Sorbonne University | 2024", body="XGBoost pipeline integrating DNA methylation, CNV, mRNA, and miRNA data for subtype classification. Balanced multiclass accuracy: 0.90."),
]

story += section("Awards and Distinctions")
story += [
    p("&bull; Best Thesis Award, Sorbonne University.", styles["Body"]),
    p("&bull; Ranked 2nd in the MAIA Brain Tissue Segmentation Challenge, University of Girona.", styles["Body"]),
    p("&bull; Erasmus Mundus Scholarship awarded by the European Union.", styles["Body"]),
    p("&bull; Summa Cum Laude, United International University.", styles["Body"]),
]

doc.build(story)
print(PDF_PATH)
