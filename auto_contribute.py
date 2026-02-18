import subprocess
import sys
import os
import time
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
    """Aktifkan ANSI escape di Windows CMD."""
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
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def run_git(args):
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
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
    w = max(len(l) for l in lines) + 4
    print(f"\n  {color}╔{'═' * w}╗{C.RESET}")
    for l in lines:
        pad = w - len(l) - 2
        print(f"  {color}║{C.RESET}  {l}{' ' * pad}  {color}║{C.RESET}")
    print(f"  {color}╚{'═' * w}╝{C.RESET}\n")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    enable_ansi()
    cls()

    # ── Banner ────────────────────────────────
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
               "folder ini adalah git repo" if is_repo else "BUKAN git repo — jalankan: git init")

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
            "   Hubungkan dulu: git remote add origin <URL>",
        ], C.YELLOW)

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
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.txt")
    berhasil = 0
    gagal    = 0

    for i in range(1, jumlah + 1):
        timestamp  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry      = f"[{timestamp}] Contribute #{i}\n"

        with open(data_file, "a", encoding="utf-8") as f:
            f.write(entry)

        code_add, _, err_add = run_git(["add", "data.txt"])
        if code_add != 0:
            print(f"\n  {C.RED}✘  [{i}/{jumlah}] git add gagal: {err_add}{C.RESET}")
            gagal += 1
            continue

        commit_msg = f"contribute: update #{i} - {timestamp}"
        code_commit, _, err_commit = run_git(["commit", "-m", commit_msg])
        if code_commit != 0:
            print(f"\n  {C.RED}✘  [{i}/{jumlah}] commit gagal: {err_commit}{C.RESET}")
            gagal += 1
            continue

        berhasil += 1
        bar_line = progress_bar(i, jumlah)
        print(f"\r{bar_line}  {C.DIM}{timestamp}{C.RESET}  ", end="", flush=True)

    print(f"\n")

    # ── Ringkasan ─────────────────────────────
    print(DIVIDER_THICK)
    print()
    print(f"  {C.BOLD}{C.WHITE}📊  HASIL{C.RESET}")
    print(DIVIDER_THIN)
    print()

    summary_lines = [
        f"✅  Commit Berhasil  :  {C.GREEN}{C.BOLD}{berhasil}{C.RESET}",
    ]
    if gagal:
        summary_lines.append(f"❌  Commit Gagal     :  {C.RED}{C.BOLD}{gagal}{C.RESET}")

    for l in summary_lines:
        print(f"  {l}")

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
    print(f"\n  {C.GREEN}{C.BOLD}�  Terima kasih sudah menggunakan GitHub Greener!{C.RESET}")
    print(f"  {C.DIM}github.com/LippyyDev/Github-Greener{C.RESET}\n")
    print(DIVIDER_THICK)
    print()
    input(f"  {C.DIM}Tekan Enter untuk keluar...{C.RESET}")


if __name__ == "__main__":
    main()
