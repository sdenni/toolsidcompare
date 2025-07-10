import csv
from config import to_be_checked
from collections import defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
RESULT_FILE = Path(__file__).parent.parent / "result" / "comparison.md"
RESULT_HTML_FILE = Path(__file__).parent.parent / "result" / "comparison.html"
RESULT_FILE_RESUME = Path(__file__).parent.parent / "result" / "comparison_resume.md"
RESULT_HTML_FILE_RESUME = Path(__file__).parent.parent / "result" / "comparison_resume.html"

CHECK = "✔️"
CROSS = "❌"

def load_ids(fileinfo):
    filepath = DATA_DIR / fileinfo["filename"]
    delimiter = fileinfo["delimiter"]
    ids = {
        "idcalonmahasiswa": set(),
        "idmahasiswa": set()
    }

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            # Lewati baris kosong atau baris pendek
            if not row or len(row) < max(
                (fileinfo["idcalonmahasiswa"] or 0),
                (fileinfo["idmahasiswa"] or 0)
            ) + 1:
                continue
            if fileinfo.get("idcalonmahasiswa") is not None:
                ids["idcalonmahasiswa"].add(row[fileinfo["idcalonmahasiswa"]].strip())
            if fileinfo.get("idmahasiswa") is not None:
                ids["idmahasiswa"].add(row[fileinfo["idmahasiswa"]].strip())

    return ids


def prepare_comparison_data(data_by_file):
    """Mempersiapkan data untuk perbandingan dengan mengumpulkan semua ID unik dan file terkait"""
    all_ids = {
        "idcalonmahasiswa": set(),
        "idmahasiswa": set()
    }
    filenames_by_type = {
        "idcalonmahasiswa": [],
        "idmahasiswa": []
    }

    for fname, ids in data_by_file.items():
        for id_type in ["idcalonmahasiswa", "idmahasiswa"]:
            if ids[id_type]:
                all_ids[id_type].update(ids[id_type])
                filenames_by_type[id_type].append(fname)

    return all_ids, filenames_by_type


def generate_comparison_table(data_by_file, all_ids, filenames, id_type, format_type="markdown"):
    """Membuat tabel perbandingan dalam format markdown atau HTML"""
    if not filenames:
        return ""
    
    title_map = {
        "idcalonmahasiswa": "ID Calon Mahasiswa",
        "idmahasiswa": "ID Mahasiswa"
    }
    title = title_map[id_type]
    
    if format_type == "markdown":
        lines = [f"## {title}\n"]
        lines.append(f"| {id_type} | " + " | ".join(filenames) + " |")
        lines.append("|" + "-" * (len(id_type) + 2) + "|" + "|".join(["---"] * len(filenames)) + "|")
        
        for id_ in sorted(all_ids[id_type]):
            row = [id_]
            for fname in filenames:
                icon = CHECK if id_ in data_by_file[fname][id_type] else CROSS
                row.append(icon)
            lines.append("| " + " | ".join(row) + " |")
        
        return "\n".join(lines)
    
    else:  # HTML format
        rows = [f"<h2>{title}</h2>"]
        rows.append("<table border='1' cellspacing='0' cellpadding='5'>")
        rows.append(f"<tr><th>{id_type}</th>{''.join(f'<th>{fname}</th>' for fname in filenames)}</tr>")
        
        for id_ in sorted(all_ids[id_type]):
            cells = []
            for fname in filenames:
                exists = id_ in data_by_file[fname][id_type]
                icon = "✔️" if exists else "❌"
                color = "green" if exists else "red"
                cells.append(f"<td style='color:{color}; font-weight:bold'>{icon}</td>")
            rows.append(f"<tr><td>{id_}</td>{''.join(cells)}</tr>")
        
        rows.append("</table><br>")
        return "\n".join(rows)


def generate_report(data_by_file):
    """Generate laporan dalam format Markdown"""
    all_ids, filenames_by_type = prepare_comparison_data(data_by_file)
    analysis = analyze_data(data_by_file, all_ids, filenames_by_type)
    
    lines = []
    
    # Tambahkan resume di awal
    resume = generate_resume_markdown(analysis, filenames_by_type)
    lines.append(resume)
    
    lines.append("# DAFTAR PERBANDINGAN\n")
    
    # ID Calon Mahasiswa
    table = generate_comparison_table(
        data_by_file, all_ids, filenames_by_type["idcalonmahasiswa"], 
        "idcalonmahasiswa", "markdown"
    )
    if table:
        lines.append(table)
    
    # ID Mahasiswa  
    table = generate_comparison_table(
        data_by_file, all_ids, filenames_by_type["idmahasiswa"],
        "idmahasiswa", "markdown"
    )
    if table:
        lines.append(f"\n{table}")
    
    return "\n".join(lines)


def generate_html_report(data_by_file):
    """Generate laporan dalam format HTML"""
    all_ids, filenames_by_type = prepare_comparison_data(data_by_file)
    analysis = analyze_data(data_by_file, all_ids, filenames_by_type)
    
    html = [
        "<html><head><meta charset='UTF-8'><title>Perbandingan Data Mahasiswa</title></head><body>"
    ]
    
    # Tambahkan resume di awal
    resume = generate_resume_html(analysis, filenames_by_type)
    html.append(resume)
    
    html.append("<h1>DAFTAR PERBANDINGAN</h1>")
    
    # ID Calon Mahasiswa
    table = generate_comparison_table(
        data_by_file, all_ids, filenames_by_type["idcalonmahasiswa"],
        "idcalonmahasiswa", "html"
    )
    if table:
        html.append(table)
    
    # ID Mahasiswa
    table = generate_comparison_table(
        data_by_file, all_ids, filenames_by_type["idmahasiswa"],
        "idmahasiswa", "html"
    )
    if table:
        html.append(table)
    
    html.append("</body></html>")
    return "\n".join(html)


def analyze_data(data_by_file, all_ids, filenames_by_type):
    """Menganalisis data untuk membuat resume statistik"""
    analysis = {
        "idcalonmahasiswa": {
            "total_unique": len(all_ids["idcalonmahasiswa"]),
            "common_ids": set(),
            "problematic_ids": []
        },
        "idmahasiswa": {
            "total_unique": len(all_ids["idmahasiswa"]),
            "common_ids": set(),
            "problematic_ids": []
        }
    }
    
    for id_type in ["idcalonmahasiswa", "idmahasiswa"]:
        filenames = filenames_by_type[id_type]
        if len(filenames) <= 1:
            continue
            
        # Cari ID yang ada di semua file
        for id_ in all_ids[id_type]:
            count = sum(1 for fname in filenames if id_ in data_by_file[fname][id_type])
            if count == len(filenames):
                analysis[id_type]["common_ids"].add(id_)
            elif count < len(filenames):
                # ID yang tidak ada di semua file (janggal)
                missing_files = [fname for fname in filenames if id_ not in data_by_file[fname][id_type]]
                analysis[id_type]["problematic_ids"].append({
                    "id": id_,
                    "missing_from": missing_files
                })
    
    return analysis


def generate_resume_markdown(analysis, filenames_by_type):
    """Generate resume dalam format Markdown"""
    lines = ["# RESUME PERBANDINGAN\n"]
    
    for id_type in ["idcalonmahasiswa", "idmahasiswa"]:
        title = "ID Calon Mahasiswa" if id_type == "idcalonmahasiswa" else "ID Mahasiswa"
        data = analysis[id_type]
        filenames = filenames_by_type[id_type]
        
        if not filenames:
            continue
            
        lines.append(f"## {title}")
        lines.append(f"- **Total ID unik**: {data['total_unique']}")
        lines.append(f"- **ID yang ada di semua file**: {len(data['common_ids'])}")
        lines.append(f"- **ID yang janggal (tidak lengkap)**: {len(data['problematic_ids'])}")
        
        if data['problematic_ids']:
            lines.append(f"\n### ID Janggal {title}:")
            for item in data['problematic_ids']:
                missing_str = ", ".join(item['missing_from'])
                lines.append(f"- **{item['id']}** tidak ada di file: {missing_str}")
        
        lines.append("")
    
    return "\n".join(lines)


def generate_resume_html(analysis, filenames_by_type):
    """Generate resume dalam format HTML"""
    html = ["<h1>RESUME PERBANDINGAN</h1>"]
    
    for id_type in ["idcalonmahasiswa", "idmahasiswa"]:
        title = "ID Calon Mahasiswa" if id_type == "idcalonmahasiswa" else "ID Mahasiswa"
        data = analysis[id_type]
        filenames = filenames_by_type[id_type]
        
        if not filenames:
            continue
            
        html.append(f"<h2>{title}</h2>")
        html.append("<ul>")
        html.append(f"<li><strong>Total ID unik</strong>: {data['total_unique']}</li>")
        html.append(f"<li><strong>ID yang ada di semua file</strong>: {len(data['common_ids'])}</li>")
        html.append(f"<li><strong>ID yang janggal (tidak lengkap)</strong>: {len(data['problematic_ids'])}</li>")
        html.append("</ul>")
        
        if data['problematic_ids']:
            html.append(f"<h3>ID Janggal {title}:</h3>")
            html.append("<ul>")
            for item in data['problematic_ids']:
                missing_str = ", ".join(item['missing_from'])
                html.append(f"<li><strong>{item['id']}</strong> tidak ada di file: {missing_str}</li>")
            html.append("</ul>")
        
        html.append("<br>")
    
    return "\n".join(html)


def main():
    data_by_file = {}
    for fileinfo in to_be_checked:
        ids = load_ids(fileinfo)
        data_by_file[fileinfo["filename"]] = ids

    report = generate_report(data_by_file)
    RESULT_FILE.write_text(report, encoding='utf-8')
    print(f"✅ Berhasil membuat laporan di: {RESULT_FILE}")
  
    report_html = generate_html_report(data_by_file)
    RESULT_HTML_FILE.write_text(report_html, encoding='utf-8')
    print(f"✅ HTML: {RESULT_HTML_FILE}")

    # Resume statistik
    all_ids, filenames_by_type = prepare_comparison_data(data_by_file)
    analysis = analyze_data(data_by_file, all_ids, filenames_by_type)
    
    resume_markdown = generate_resume_markdown(analysis, filenames_by_type)
    RESULT_FILE_RESUME.write_text(resume_markdown, encoding='utf-8')
    print(f"✅ Berhasil membuat resume di: {RESULT_FILE_RESUME}")
    
    resume_html = generate_resume_html(analysis, filenames_by_type)
    RESULT_HTML_FILE_RESUME.write_text(resume_html, encoding='utf-8')
    print(f"✅ HTML Resume: {RESULT_HTML_FILE_RESUME}")

if __name__ == "__main__":
    main()
