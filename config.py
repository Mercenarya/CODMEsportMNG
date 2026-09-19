import os
import csv
import sys

# Đảm bảo ROOT trỏ đúng vào thư mục chứa file config.py hoặc main.py của bạn
CURRENT = os.path.dirname(os.path.abspath(__file__))

ROOT = os.path.join(CURRENT)

sys.path.append(ROOT)

MEMBERS_PATH = os.path.join(ROOT,'data','member1.csv')

MATCH_PATH = os.path.join(ROOT,'data','match.csv')

EVENT_PATH = os.path.join(ROOT,'data','events.csv')

NOTE_PATH = os.path.join(ROOT,'data','notes.csv')

PRIMUS_PATH = os.path.join(ROOT,'data','primus_members.csv')

PRIMUS_SCHEDULE_PATH = os.path.join(ROOT,'data','primus_schedule.csv')

ASPIRANTS_PATH = os.path.join(ROOT,'data','aspirants_members.csv')

ASPIRANTS_SCHEDULE_PATH = os.path.join(ROOT,'data','aspirants_schedule.csv')

PRIMUS_TACTICS_PATH = os.path.join(ROOT,'data','team_1.csv')

ASPIRANTS_TACTICS_PATH = os.path.join(ROOT,'data','team_2.csv') 
# Định nghĩa các đường dẫn tệp tin dựa trên sơ đồ của bạn
CSV_PATHS = {
    "member1.csv": (os.path.join(ROOT, 'data', 'member1.csv'), 
                    ["ID", "Full Name", "Role", "Email", "Status"]),
                    
    "match.csv": (os.path.join(ROOT, 'data', 'match.csv'), 
                  ["Match ID", "Opponent", "Date", "Time", "Result"]),
                  
    "events.csv": (os.path.join(ROOT, 'data', 'events.csv'), 
                   ["Event ID", "Title", "Location", "Date", "Description"]),
                   
    "notes.csv": (os.path.join(ROOT, 'data', 'notes.csv'), 
                  ["Note ID", "Title", "Content", "Created Date"]),
                  
    "primus_members.csv": (os.path.join(ROOT, 'data', 'primus_members.csv'), 
                           ["Member ID", "Name", "Role", "Specialty", "Rank"]),
                           
    "primus_schedule.csv": (os.path.join(ROOT, 'data', 'primus_schedule.csv'), 
                            ["Schedule ID", "Activity", "Date", "Time", "Status"]),
                            
    "aspirants_members.csv": (os.path.join(ROOT, 'data', 'aspirants_members.csv'), 
                              ["Member ID", "Name", "Role", "Specialty", "Rank"]),
                              
    "aspirants_schedule.csv": (os.path.join(ROOT, 'data', 'aspirants_schedule.csv'), 
                               ["Schedule ID", "Activity", "Date", "Time", "Status"]),
                               
    "team_1.csv": (os.path.join(ROOT, 'data', 'team_1.csv'), 
                   ["Tactic ID", "Name", "Formation", "Strategy", "Last Updated"]),
                   
    "team_2.csv": (os.path.join(ROOT, 'data', 'team_2.csv'), 
                   ["Tactic ID", "Name", "Formation", "Strategy", "Last Updated"])
}

def initialize_system_csvs():
    """
    Tự động quét và khởi tạo các file CSV hệ thống 
    nếu chúng chưa tồn tại trong thư mục 'data'.
    """
    data_dir = os.path.join(ROOT, 'data')
    
    try:
        # Tạo thư mục data nếu chưa tồn tại
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            print(f"[INFO] Created directory: {data_dir}")

        # Duyệt qua từng file để kiểm tra và khởi tạo tiêu đề cột (Headers)
        for file_name, (file_path, headers) in CSV_PATHS.items():
            if not os.path.exists(file_path):
                # Sử dụng newline="" để tránh bị chèn thêm dòng trống trên Windows
                with open(file_path, mode="w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers) # Chỉ ghi dòng tiêu đề ban đầu (file trắng hoàn toàn)
                print(f"[SUCCESS] Initialized missing file: {file_name}")
            else:
                print(f"[INFO] File already exists: {file_name}")
                
    except Exception as e:
        print(f"[ERROR] Failed to initialize system CSV files: {str(e)}")

# Tự động chạy khi file này được thực thi trực tiếp
# if __name__ == "__main__":
#     initialize_system_csvs()