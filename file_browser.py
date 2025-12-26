import os
from flask import Blueprint, jsonify, send_from_directory, abort

file_api = Blueprint("file_api", __name__)

BASE_FOLDER = r"D:\MCA2025-27\20MCA105 - ADVANCED DATA STRUCTURES"

@file_api.route("/files", defaults={"subpath": ""})
@file_api.route("/files/<path:subpath>")
def list_files(subpath):
    folder_path = os.path.join(BASE_FOLDER, subpath)

    if not os.path.isdir(folder_path):
        return jsonify([])

    items = []
    for name in os.listdir(folder_path):
        full_path = os.path.join(folder_path, name)
        items.append({
            "name": name,
            "type": "folder" if os.path.isdir(full_path) else "file",
            "path": "/".join(filter(None, [subpath, name]))
        })

    return jsonify(items)

@file_api.route("/open/<path:filepath>")
def open_file(filepath):
    try:
        return send_from_directory(BASE_FOLDER, filepath, as_attachment=False)
    except:
        abort(404)
