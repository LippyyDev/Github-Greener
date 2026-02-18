import subprocess
import sys
import os
import time
import random
from datetime import datetime


# ─────────────────────────────────────────────
#  ANSI COLOR CODES
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    BLUE    = "\033[94m"
    BG_GREEN  = "\033[42m"
    BG_BLACK  = "\033[40m"


def enable_ansi():
    if sys.platform == "win32":
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def cls():
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────────
#  ASCII BANNER
# ─────────────────────────────────────────────
BANNER = f"""
{C.GREEN}{C.BOLD}
  ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗
 {C.CYAN} ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗
{C.GREEN}  ██║  ███╗██║   ██║   ███████║██║   ██║██████╔╝
{C.CYAN}  ██║   ██║██║   ██║   ██╔══██║██║   ██║██╔══██╗
{C.GREEN}  ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝
{C.CYAN}   ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
{C.RESET}
{C.GREEN}  ██████╗ ██████╗ ███████╗███████╗███╗   ██╗███████╗██████╗
{C.CYAN}  ██╔════╝ ██╔══██╗██╔════╝██╔════╝████╗  ██║██╔════╝██╔══██╗
{C.GREEN}  ██║  ███╗██████╔╝█████╗  █████╗  ██╔██╗ ██║█████╗  ██████╔╝
{C.CYAN}  ██║   ██║██╔══██╗██╔══╝  ██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗
{C.GREEN}  ╚██████╔╝██║  ██║███████╗███████╗██║ ╚████║███████╗██║  ██║
{C.CYAN}   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{C.RESET}"""

TAGLINE = f"  {C.DIM}{C.WHITE}🌿  Auto GitHub Contribution Tool  |  by LippyyDev{C.RESET}"
DIVIDER_THICK = f"{C.DIM}{C.GREEN}  {'═' * 60}{C.RESET}"
DIVIDER_THIN  = f"{C.DIM}{C.CYAN}  {'─' * 60}{C.RESET}"


# ─────────────────────────────────────────────
#  PESAN COMMIT NATURAL (ANTI-SPAM)
# ─────────────────────────────────────────────
COMMIT_MESSAGES = [
    "fix: perbaiki logika validasi input",
    "refactor: sederhanakan struktur kode",
    "docs: perbarui catatan penggunaan",
    "chore: bersihkan kode yang tidak terpakai",
    "style: rapikan indentasi dan spasi",
    "fix: tangani edge case pada parsing data",
    "feat: tambah pengecekan kondisi awal",
    "refactor: pisahkan fungsi agar lebih modular",
    "docs: tambah komentar penjelasan fungsi",
    "chore: update dependensi minor",
    "fix: perbaiki typo pada pesan error",
    "style: sesuaikan format output",
    "feat: optimalkan performa loop utama",
    "refactor: ganti nama variabel agar lebih deskriptif",
    "docs: perbarui README dengan contoh terbaru",
    "fix: atasi bug saat file kosong",
    "chore: hapus debug log yang tertinggal",
    "feat: tambah penanganan exception lebih baik",
    "style: konsistenkan penggunaan tanda kutip",
    "refactor: ekstrak konstanta ke bagian atas file",
    "fix: perbaiki kondisi batas pada iterasi",
    "docs: tambah deskripsi parameter fungsi",
    "chore: reorganisasi struktur folder",
    "feat: tambah fallback jika data tidak tersedia",
    "fix: koreksi urutan operasi pada kalkulasi",
    "refactor: kurangi duplikasi kode",
    "style: tambah baris kosong antar blok logika",
    "docs: perbaiki ejaan pada komentar",
    "chore: sinkronisasi konfigurasi lokal",
    "feat: tingkatkan keterbacaan output",
    "fix: perbaiki penanganan karakter spesial",
    "refactor: gunakan list comprehension",
    "docs: tambah contoh penggunaan di header",
    "chore: perbarui .gitignore",
    "fix: stabilkan hasil saat input tidak terduga",
    "feat: tambah pesan informatif saat proses selesai",
    "style: seragamkan panjang baris maksimum",
    "refactor: pisahkan konfigurasi dari logika utama",
    "docs: lengkapi docstring fungsi helper",
    "chore: bersihkan file sementara",
]

# ─────────────────────────────────────────────
#  FILE YANG DIMODIFIKASI (ANTI-SPAM)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_FILES = {
    "data.txt": {
        "mode": "append",
        "templates": [
            "session: {ts} | status: aktif\n",
            "log [{ts}]: proses selesai tanpa error\n",
            "entry {ts} — operasi berhasil dijalankan\n",
            "[{ts}] checkpoint tercapai\n",
            "record: {ts} | hasil: valid\n",
        ],
    },
    "notes.md": {
        "mode": "append",
        "templates": [
            "- [{ts}] Catatan sesi: semua berjalan normal\n",
            "- [{ts}] Review: tidak ada perubahan signifikan\n",
            "- [{ts}] Update kecil pada alur kerja\n",
            "- [{ts}] Penyesuaian minor pada konfigurasi\n",
            "- [{ts}] Pengecekan rutin selesai\n",
        ],
    },
    "changelog.txt": {
        "mode": "append",
        "templates": [
            "[{ts}] Perbaikan kecil pada modul utama\n",
            "[{ts}] Refaktor bagian validasi\n",
            "[{ts}] Optimasi performa minor\n",
            "[{ts}] Penyesuaian output format\n",
            "[{ts}] Pembersihan kode lama\n",
        ],
    },
    "config.ini": {
        "mode": "overwrite_section",
        "templates": [
            "[settings]\nlast_run = {ts}\nstatus = ok\nmode = auto\n",
            "[settings]\nlast_run = {ts}\nstatus = success\nmode = normal\n",
            "[settings]\nlast_run = {ts}\nstatus = completed\nmode = standard\n",
        ],
    },
}


def init_target_files():
    """Buat file-file target jika belum ada."""
    defaults = {
        "data.txt":     "# Data Log\n",
        "notes.md":     "# Catatan Proyek\n\n",
        "changelog.txt": "# Changelog\n\n",
        "config.ini":   "[settings]\nlast_run = -\nstatus = init\n",
    }
    for fname, content in defaults.items():
        fpath = os.path.join(BASE_DIR, fname)
        if not os.path.exists(fpath):
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)


def modify_random_file(ts: str) -> list[str]:
    """
    Pilih 1–2 file secara acak, modifikasi isinya,
    kembalikan daftar nama file yang diubah.
    """
    # Pilih 1 atau 2 file secara acak
    count = random.randint(1, 2)
    chosen = random.sample(list(TARGET_FILES.keys()), count)
    modified = []

    for fname in chosen:
        cfg   = TARGET_FILES[fname]
        fpath = os.path.join(BASE_DIR, fname)
        tmpl  = random.choice(cfg["templates"])
        text  = tmpl.replace("{ts}", ts)

        if cfg["mode"] == "append":
            with open(fpath, "a", encoding="utf-8") as f:
                f.write(text)
        elif cfg["mode"] == "overwrite_section":
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(text)

        modified.append(fname)

    return modified


# ─────────────────────────────────────────────
#  GIT HELPERS
# ─────────────────────────────────────────────
def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=BASE_DIR,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_git_repo():
    code, _, _ = run_git(["rev-parse", "--is-inside-work-tree"])
    return code == 0

def check_git_remote():
    code, out, _ = run_git(["remote", "-v"])
    return code == 0 and bool(out)

def check_git_user():
    code_n, name, _  = run_git(["config", "user.name"])
    code_e, email, _ = run_git(["config", "user.email"])
    return code_n == 0 and bool(name) and code_e == 0 and bool(email), name, email


# ─────────────────────────────────────────────
#  UI HELPERS
# ─────────────────────────────────────────────
def status_row(label, ok, detail=""):
    icon  = f"{C.GREEN}✔{C.RESET}" if ok else f"{C.RED}✘{C.RESET}"
    badge = f"{C.BG_GREEN}{C.BOLD}  OK  {C.RESET}" if ok else f"\033[41m{C.BOLD}  !!  {C.RESET}"
    det   = f"  {C.DIM}{C.WHITE}{detail}{C.RESET}" if detail else ""
    print(f"  {icon}  {badge}  {C.WHITE}{label}{C.RESET}{det}")


def spinner_line(msg, duration=0.8):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r  {C.CYAN}{frames[i % len(frames)]}{C.RESET}  {C.DIM}{msg}{C.RESET}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r  {C.GREEN}✔{C.RESET}  {C.DIM}{msg}{C.RESET}  ")


def progress_bar(current, total, width=40):
    filled = int(width * current / total)
    bar    = f"{C.GREEN}{'█' * filled}{C.DIM}{'░' * (width - filled)}{C.RESET}"
    pct    = int(100 * current / total)
    return f"  [{bar}] {C.BOLD}{C.WHITE}{pct:3d}%{C.RESET}  {C.CYAN}{current}/{total}{C.RESET}"


def box(lines, color=C.CYAN):
    # Strip ANSI untuk hitung lebar asli
    import re
    ansi_escape = re.compile(r'\033\[[0-9;]*m')
    w = max(len(ansi_escape.sub('', l)) for l in lines) + 4
    print(f"\n  {color}╔{'═' * w}╗{C.RESET}")
    for l in lines:
        clean_len = len(ansi_escape.sub('', l))
        pad = w - clean_len - 2
        print(f"  {color}║{C.RESET}  {l}{' ' * pad}  {color}║{C.RESET}")
    print(f"  {color}╚{'═' * w}╝{C.RESET}\n")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    enable_ansi()
    cls()

    print(BANNER)
    print(TAGLINE)
    print()
    print(DIVIDER_THICK)
    print()

    # ── Deteksi Git ───────────────────────────
    print(f"  {C.BOLD}{C.WHITE}📋  PEMERIKSAAN SISTEM{C.RESET}")
    print(DIVIDER_THIN)
    print()

    spinner_line("Mendeteksi git repository...", 0.6)

    is_repo = check_git_repo()
    status_row("Git Repository", is_repo,
               "folder ini adalah git repo" if is_repo else "BUKAN git repo")

    if not is_repo:
        box([
            "❌  Folder ini belum diinisialisasi sebagai git repo.",
            "",
            "   Jalankan perintah berikut:",
            "   > git init",
            "   > git remote add origin <URL_REPO>",
        ], C.RED)
        input(f"  {C.DIM}Tekan Enter untuk keluar...{C.RESET}")
        sys.exit(1)

    has_remote = check_git_remote()
    _, remote_out, _ = run_git(["remote", "-v"])
    remote_url = remote_out.split("\n")[0].split()[1] if remote_out else "-"
    status_row("Remote (origin)", has_remote,
               remote_url if has_remote else "belum ada remote")

    user_ok, git_name, git_email = check_git_user()
    status_row("Git User", user_ok,
               f"{git_name} <{git_email}>" if user_ok else "belum dikonfigurasi")

    print()

    if not user_ok:
        box([
            "❌  Git user belum dikonfigurasi.",
            "",
            "   Jalankan:",
            '   > git config --global user.name  "Nama Kamu"',
            '   > git config --global user.email "email@kamu.com"',
        ], C.RED)
        input(f"  {C.DIM}Tekan Enter untuk keluar...{C.RESET}")
        sys.exit(1)

    if not has_remote:
        box([
            "⚠️   Tidak ada remote. Commit akan disimpan lokal.",
            "   Hubungkan: git remote add origin <URL>",
        ], C.YELLOW)

    # ── Inisialisasi file target ───────────────
    init_target_files()

    # ── Input jumlah commit ───────────────────
    print(DIVIDER_THICK)
    print()
    print(f"  {C.BOLD}{C.WHITE}🔢  KONFIGURASI CONTRIBUTE{C.RESET}")
    print(DIVIDER_THIN)
    print()

    while True:
        try:
            raw = input(f"  {C.CYAN}➤{C.RESET}  Jumlah contribute yang diinginkan: {C.BOLD}{C.WHITE}")
            print(C.RESET, end="")
            jumlah = int(raw)
            if jumlah <= 0:
                print(f"  {C.YELLOW}⚠  Masukkan angka lebih dari 0.{C.RESET}\n")
                continue
            break
        except ValueError:
            print(f"  {C.RED}✘  Input tidak valid. Masukkan angka bulat.{C.RESET}\n")

    print()
    print(DIVIDER_THICK)
    print()
    print(f"  {C.BOLD}{C.WHITE}🚀  MEMULAI {jumlah} COMMIT{C.RESET}")
    print(DIVIDER_THIN)
    print()

    # ── Loop commit ───────────────────────────
    berhasil = 0
    gagal    = 0
    used_msgs = []

    for i in range(1, jumlah + 1):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Modifikasi file secara acak
        modified_files = modify_random_file(timestamp)

        # git add file yang dimodifikasi
        code_add, _, err_add = run_git(["add"] + modified_files)
        if code_add != 0:
            print(f"\n  {C.RED}✘  [{i}/{jumlah}] git add gagal: {err_add}{C.RESET}")
            gagal += 1
            continue

        # Pilih pesan commit natural, hindari duplikat berturut-turut
        available = [m for m in COMMIT_MESSAGES if m not in used_msgs[-3:]]
        if not available:
            available = COMMIT_MESSAGES
        commit_msg = random.choice(available)
        used_msgs.append(commit_msg)

        code_commit, _, err_commit = run_git(["commit", "-m", commit_msg])
        if code_commit != 0:
            print(f"\n  {C.RED}✘  [{i}/{jumlah}] commit gagal: {err_commit}{C.RESET}")
            gagal += 1
            continue

        berhasil += 1
        files_str = f"{C.DIM}({', '.join(modified_files)}){C.RESET}"
        bar_line  = progress_bar(i, jumlah)
        print(f"\r{bar_line}  {files_str}  ", end="", flush=True)

    print(f"\n")

    # ── Ringkasan ─────────────────────────────
    print(DIVIDER_THICK)
    print()
    print(f"  {C.BOLD}{C.WHITE}📊  HASIL{C.RESET}")
    print(DIVIDER_THIN)
    print()
    print(f"  {C.GREEN}✔{C.RESET}  Commit Berhasil  :  {C.GREEN}{C.BOLD}{berhasil}{C.RESET}")
    if gagal:
        print(f"  {C.RED}✘{C.RESET}  Commit Gagal     :  {C.RED}{C.BOLD}{gagal}{C.RESET}")
    print()

    # ── Push ──────────────────────────────────
    if has_remote and berhasil > 0:
        print(DIVIDER_THIN)
        print()
        push = input(f"  {C.CYAN}➤{C.RESET}  Push ke GitHub sekarang? {C.DIM}(y/n){C.RESET}: {C.BOLD}{C.WHITE}").strip().lower()
        print(C.RESET, end="")
        print()

        if push == "y":
            spinner_line("Mendorong commit ke remote...", 1.0)

            code_push, _, err_push = run_git(["push"])
            if code_push == 0:
                box([
                    "🎉  Push berhasil!",
                    "",
                    f"   {berhasil} commit telah dikirim ke GitHub.",
                    "   Cek contribution graph kamu sekarang!",
                ], C.GREEN)
            else:
                _, branch, _ = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
                code_push2, _, err_push2 = run_git(["push", "--set-upstream", "origin", branch])
                if code_push2 == 0:
                    box([
                        f"🎉  Push berhasil ke branch '{branch}'!",
                        "",
                        f"   {berhasil} commit telah dikirim ke GitHub.",
                        "   Cek contribution graph kamu sekarang!",
                    ], C.GREEN)
                else:
                    box([
                        "❌  Push gagal.",
                        f"   {err_push2}",
                    ], C.RED)
        else:
            print(f"  {C.DIM}Commit disimpan lokal. Push manual: git push{C.RESET}\n")
    elif berhasil > 0:
        box([
            "ℹ️   Commit tersimpan secara lokal.",
            "   Hubungkan remote lalu jalankan: git push",
        ], C.YELLOW)

    print(DIVIDER_THICK)
    print(f"\n  {C.GREEN}{C.BOLD}🌿  Terima kasih sudah menggunakan GitHub Greener!{C.RESET}")
    print(f"  {C.DIM}github.com/LippyyDev/Github-Greener{C.RESET}\n")
    print(DIVIDER_THICK)
    print()
    input(f"  {C.DIM}Tekan Enter untuk keluar...{C.RESET}")


if __name__ == "__main__":
    main()
