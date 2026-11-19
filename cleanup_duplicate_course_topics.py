"""
Cleanup script to resolve duplicate modules/topics from initial ingestion
while strictly preserving all 191 student progress records.
"""
import sqlite3

def cleanup():
    db_path = "instance/trackmycourse.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Verify user_progress count before
    cur.execute("SELECT count(*) FROM user_progress")
    initial_up = cur.fetchone()[0]
    print(f"Initial user_progress records: {initial_up}")
    assert initial_up == 191, f"Expected 191 user_progress records, found {initial_up}"

    # 2. Duplicate module IDs to remove for courses 3, 4, 5, 6
    dup_mod_ids = [66, 67, 68, 69, 70, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 135, 136, 137, 138, 139]
    cur.execute(f"DELETE FROM topic WHERE module_id IN ({','.join(map(str, dup_mod_ids))})")
    print(f"Deleted topics from duplicate modules.")

    cur.execute(f"DELETE FROM module WHERE id IN ({','.join(map(str, dup_mod_ids))})")
    print(f"Deleted duplicate module rows.")

    # 3. For Course 7 (modules 21..25), delete topics >= 500
    cur.execute("DELETE FROM topic WHERE module_id IN (21, 22, 23, 24, 25) AND id >= 500")
    print(f"Deleted appended duplicate topics for Course 7.")

    # 4. Set module_no for modules 1..20
    for idx, mid in enumerate(range(1, 6), 1):
        cur.execute("UPDATE module SET module_no = ? WHERE id = ?", (idx, mid))
    for idx, mid in enumerate(range(6, 11), 1):
        cur.execute("UPDATE module SET module_no = ? WHERE id = ?", (idx, mid))
    for idx, mid in enumerate(range(11, 16), 1):
        cur.execute("UPDATE module SET module_no = ? WHERE id = ?", (idx, mid))
    for idx, mid in enumerate(range(16, 21), 1):
        cur.execute("UPDATE module SET module_no = ? WHERE id = ?", (idx, mid))
    print("Set module_no (1..5) for original modules 1..20.")

    # 5. Verify user_progress count after
    cur.execute("SELECT count(*) FROM user_progress")
    final_up = cur.fetchone()[0]
    print(f"Final user_progress records: {final_up}")
    assert final_up == 191, f"User progress changed! Expected 191, got {final_up}"

    conn.commit()
    conn.close()
    print("Cleanup committed successfully.")

if __name__ == "__main__":
    cleanup()
