import os
from pathlib import Path

# pypdf のインポート（バージョンに合わせて自動判別）
try:
    from pypdf import PdfMerger
    MERGER_CLASS = PdfMerger
    print("pypdf (最新版) を使用します")
except ImportError:
    try:
        from PyPDF2 import PdfMerger
        MERGER_CLASS = PdfMerger
        print("PyPDF2 を使用します")
    except ImportError:
        try:
            from pypdf import PdfWriter
            # 古いバージョン用
            print("pypdf (旧版) を使用します")
            MERGER_CLASS = None
        except ImportError:
            print("エラー: pypdf または PyPDF2 がインストールされていません")
            print("以下のコマンドでインストールしてください:")
            print("  pip install pypdf")
            exit(1)

# 設定
source_folder = r"C:\c_wk\10_会社\PDF-相关\pypdf\1-結合\1"
output_folder = r"C:\c_wk\10_会社\PDF-相关\pypdf\新しいフォルダー"
year_month = "202606"

print("=" * 50)
print("  PDF 自動結合ツール（フォルダ1 + フォルダ2）")
print("=" * 50)
print()

# 出力フォルダ作成
os.makedirs(output_folder, exist_ok=True)

# PDFファイルをグループ化（スペースより前の名前で）
pdf_groups = {}
for pdf_file in Path(source_folder).glob("*.pdf"):
    base_name = pdf_file.stem.split()[0]  # スペースより前を取得
    if base_name not in pdf_groups:
        pdf_groups[base_name] = []
    pdf_groups[base_name].append(pdf_file)

print(f"見つかったPDFファイル: {sum(len(files) for files in pdf_groups.values())} 個")
print(f"結合グループ数: {len(pdf_groups)} グループ")
print()

# 各グループを結合
merged_count = 0
for base_name, pdf_files in sorted(pdf_groups.items()):
    output_filename = f"{base_name}({year_month}).pdf"
    output_path = os.path.join(output_folder, output_filename)
    
    try:
        if MERGER_CLASS:
            # PdfMerger を使用（推奨）
            merger = MERGER_CLASS()
            
            # ソートして結合（一貫性のため）
            for pdf_path in sorted(pdf_files):
                print(f"  追加: {pdf_path.name}")
                merger.append(str(pdf_path))
            
            merger.write(output_path)
            merger.close()
        else:
            # 旧版 pypdf 用（PdfWriter）
            from pypdf import PdfWriter, PdfReader
            
            writer = PdfWriter()
            
            for pdf_path in sorted(pdf_files):
                print(f"  追加: {pdf_path.name}")
                reader = PdfReader(str(pdf_path))
                for page in reader.pages:
                    writer.add_page(page)
            
            with open(output_path, "wb") as f:
                writer.write(f)
        
        merged_count += 1
        print(f"✓ 作成: {output_filename} ({len(pdf_files)}個のファイルを結合)")
        print()
        
    except Exception as e:
        print(f"✗ エラー: {output_filename} の作成に失敗しました")
        print(f"  エラー詳細: {str(e)}")
        print()

print("=" * 50)
print(f"完了！{merged_count}個のPDFファイルを作成しました。")
print(f"保存先: {output_folder}")
print("=" * 50)