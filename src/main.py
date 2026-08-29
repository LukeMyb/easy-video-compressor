import sys
import os
import subprocess
import glob

# プロジェクトルートと各フォルダのパス定義
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
INPUT_DIR = os.path.join(PROJECT_ROOT, "input")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

FFMPEG_PATH = os.path.join(BIN_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(BIN_DIR, "ffprobe.exe")

def get_video_duration(input_path):
    """ffprobeを使用して動画の長さを取得する"""
    cmd = [
        FFPROBE_PATH,
        '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', input_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        return float(result.stdout.strip())
    except ValueError:
        print("エラー: 動画の長さを取得できませんでした。ffprobeが正しくインストールされているか確認してください。")
        sys.exit(1)

def compress_video(input_path):
    # 安全マージンを取って9.0MBを目標サイズに設定
    target_size_mb = 9.0
    audio_bitrate_kbps = 128

    duration = get_video_duration(input_path)
    
    # 目標総ビットレート (kbps) = (目標サイズ(MB) * 8192(kb/MB)) / 秒数
    target_total_bitrate_kbps = (target_size_mb * 8192) / duration
    target_video_bitrate_kbps = int(target_total_bitrate_kbps - audio_bitrate_kbps)

    if target_video_bitrate_kbps <= 0:
        print(f"エラー: 動画が長すぎるため、10MB以下に圧縮できません。({input_path})") # ★変更
        return

    # outputフォルダへの出力パス生成
    basename = os.path.basename(input_path)
    filename, ext = os.path.splitext(basename)
    output_path = os.path.join(OUTPUT_DIR, f"{filename}_discord.mp4")

    print(f"動画の長さ: {duration:.2f}秒")
    print(f"目標ビデオビットレート: {target_video_bitrate_kbps} kbps")

    # 1パス目（分析）
    cmd_pass1 = [
        FFMPEG_PATH,
        '-y', '-i', input_path,
        '-c:v', 'libx264',
        '-b:v', f'{target_video_bitrate_kbps}k',
        '-pass', '1',
        '-an', '-f', 'mp4', 'NUL'
    ]

    # 2パス目（エンコード）
    cmd_pass2 = [
        FFMPEG_PATH,
        '-y', '-i', input_path,
        '-c:v', 'libx264',
        '-b:v', f'{target_video_bitrate_kbps}k',
        '-pass', '2',
        '-c:a', 'aac',
        '-b:a', f'{audio_bitrate_kbps}k',
        output_path
    ]

    print("パス1を実行中...")
    subprocess.run(cmd_pass1, check=True)

    print("パス2を実行中...")
    subprocess.run(cmd_pass2, check=True)

    # 2パスエンコードで生成されるログファイルの削除
    for log_file in ['ffmpeg2pass-0.log', 'ffmpeg2pass-0.log.mbtree']:
        if os.path.exists(log_file):
            os.remove(log_file)

    print(f"圧縮完了: {output_path}")

# inputディレクトリ内のファイルを一括処理する関数
def process_all_videos():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    if not os.path.exists(FFMPEG_PATH) or not os.path.exists(FFPROBE_PATH):
        print("エラー: bin/ フォルダに ffmpeg.exe と ffprobe.exe が存在するか確認してください。")
        sys.exit(1)

    # inputフォルダ内の主要な動画ファイルを対象とする
    extensions = ('*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv')
    video_files = []
    for ext in extensions:
        video_files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))

    if not video_files:
        print(f"{INPUT_DIR} フォルダに動画ファイルが見つかりません。")
        return

    for video_file in video_files:
        print("============================================================")
        print(f"処理中: {video_file}")
        compress_video(video_file)
    print("============================================================")
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    process_all_videos()