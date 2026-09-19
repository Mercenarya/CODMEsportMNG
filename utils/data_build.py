import os
import json

# Định nghĩa các thư mục và đường dẫn file cấu hình mặc định
ROOT_DIR = os.getcwd()
CONFIG_DIR = os.path.join(ROOT_DIR, "config")

# Định nghĩa danh sách các file cấu hình cần có và nội dung mặc định của chúng
DEFAULT_CONFIGS = {
    # 1. File cấu hình ứng dụng chung (JSON)
    os.path.join(CONFIG_DIR, "settings.json"): {
        "app_name": "Illuminati Management App",
        "version": "2.1.0",
        "theme_mode": "dark",
        "language": "en",
        "database": {
            "type": "sqlite",
            "db_name": "database.db"
        }
    },
    # 2. File cấu hình kết nối API hoặc Token (JSON)
    os.path.join(CONFIG_DIR, "api_config.json"): {
        "meta_ads_api": {
            "access_token": "",
            "act_id": "",
            "app_id": ""
        },
        "pancake_api": {
            "token": ""
        }
    }
}

def initialize_configurations():
    """
    Kiểm tra và tự động tạo thư mục config cùng các file cấu hình mặc định
    nếu chúng chưa tồn tại trên hệ thống.
    """
    try:
        # 1. Tạo thư mục config nếu chưa có
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)
            print(f"[INFO] Created config directory at: {CONFIG_DIR}")

        # 2. Kiểm tra từng file và ghi nội dung mặc định nếu thiếu
        for file_path, default_content in DEFAULT_CONFIGS.items():
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as f:
                    # Ghi dữ liệu dạng JSON được format đẹp mắt (indent=4)
                    json.dump(default_content, f, indent=4, ensure_ascii=False)
                print(f"[SUCCESS] Initialized missing config file: {os.path.basename(file_path)}")
            else:
                print(f"[INFO] Config file already exists: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"[ERROR] Failed to initialize configurations: {str(e)}")

# Tự động chạy khởi tạo khi file config.py này được import hoặc thực thi trực tiếp
if __name__ == "__main__":
    initialize_configurations()