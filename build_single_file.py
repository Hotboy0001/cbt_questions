import os
import base64
import re

SOURCE_DIR = '.'
BUILD_NAME = 'offline_cbt.html'

def build():
    html_files = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.html') and f != 'index.html' and f != BUILD_NAME]
    
    # 1. Read all exam files, strip webhook and inject localstorage bypass, then base64 encode
    exams_data = {}
    
    localstorage_override = """
<script>
// OFFLINE OVERRIDE: Prevent lockouts
(function() {
    var originalGetItem = localStorage.getItem;
    localStorage.getItem = function(key) {
        if (!key) return null;
        if (key === 'shis_cbt_completed_status' || key.startsWith('submitted_') || key.startsWith('CBT_LOCK_') || key.startsWith('SHIS_PENALTY_') || key.startsWith('shis_submission_log_')) {
            return null;
        }
        return originalGetItem.apply(this, arguments);
    };
    var originalSetItem = localStorage.setItem;
    localStorage.setItem = function(key, value) {
        if (!key) return;
        if (key === 'shis_cbt_completed_status' || key.startsWith('submitted_') || key.startsWith('CBT_LOCK_') || key.startsWith('SHIS_PENALTY_') || key.startsWith('shis_submission_log_')) {
            return; // Block saving lockouts
        }
        originalSetItem.apply(this, arguments);
    };
})();
</script>
"""

    for f in html_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        content = content.replace('<head>', '<head>\n' + localstorage_override, 1)
        content = re.sub(r'<!-- SHIS Webhook Engine -->.*?<\/script>', '', content, flags=re.DOTALL)
        
        # Base64 encode
        b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        exams_data[f] = b64
        
    # 2. Read index.html
    with open('index.html', 'r', encoding='utf-8') as file:
        index_content = file.read()
        
    # Remove webhook from index.html
    index_content = re.sub(r'<!-- SHIS Webhook Engine -->.*?<\/script>', '', index_content, flags=re.DOTALL)
    
    # Inject the examsData object into index.html
    exams_js = "const examsData = {\n"
    for filename, b64 in exams_data.items():
        # EncodeURI for safety if there are weird characters in filenames
        exams_js += f'    "{filename}": "{b64}",\n'
    exams_js += "};\n"
    
    # We replace window.location.href = encodeURI(targetFile); with the iframe injection
    iframe_logic = """
            if (examsData[targetFile]) {
                document.body.innerHTML = '';
                var iframe = document.createElement('iframe');
                iframe.style.width = '100vw';
                iframe.style.height = '100vh';
                iframe.style.border = 'none';
                iframe.src = "data:text/html;base64," + examsData[targetFile];
                document.body.style.margin = '0';
                document.body.appendChild(iframe);
            } else {
                alert("Exam file not found in offline bundle.");
            }
"""
    index_content = index_content.replace('window.location.href = encodeURI(targetFile);', iframe_logic)
    
    # Inject examsData before the iframe logic
    index_content = index_content.replace('// Redirect to the exam file', exams_js + '\n            // Load into Iframe')
    
    auth_overlay = """
<div id="offline-auth-overlay" style="position:fixed;top:0;left:0;width:100%;height:100%;background:#f5f7fa;z-index:999999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Segoe UI', sans-serif;">
    <h2 style="color:#0d47a1;margin-bottom:20px;font-size:28px;">STANDARD HEIGHT OFFLINE CBT</h2>
    <p style="margin-bottom:15px;color:#333;font-size:16px;">Enter Authorization PIN (Time) to proceed.</p>
    <input type="password" id="offline-pin" placeholder="PIN" style="padding:12px;font-size:20px;border:2px solid #cfd8dc;border-radius:8px;margin-bottom:15px;text-align:center;width:250px;outline:none;">
    <button onclick="checkOfflinePin()" style="padding:12px 30px;background:#0d47a1;color:white;border:none;border-radius:8px;font-size:18px;cursor:pointer;font-weight:600;box-shadow:0 4px 6px rgba(0,0,0,0.1);">Unlock Portal</button>
    <p id="offline-err" style="color:#d32f2f;display:none;margin-top:15px;font-weight:500;">Incorrect PIN. Access Denied.</p>
</div>
<script>
function checkOfflinePin() {
    var input = document.getElementById('offline-pin').value.trim();
    var now = new Date();
    var h24 = now.getHours();
    var h12 = h24 % 12 || 12;
    var m = now.getMinutes();
    
    function pad(n) { return n < 10 ? '0' + n : n; }
    
    var valid1 = pad(h12) + "" + pad(m);
    var valid2 = pad(h24) + "" + pad(m);
    
    if (input === valid1 || input === valid2) {
        var overlay = document.getElementById('offline-auth-overlay');
        overlay.style.opacity = '0';
        setTimeout(function() { overlay.style.display = 'none'; }, 300);
    } else {
        document.getElementById('offline-err').style.display = 'block';
    }
}
</script>
"""
    # Inject auth overlay
    index_content = index_content.replace('<body>', '<body>\n' + auth_overlay, 1)
    
    with open(BUILD_NAME, 'w', encoding='utf-8') as out:
        out.write(index_content)
        
    print(f"Successfully generated {BUILD_NAME} with {len(html_files)} embedded exams.")

if __name__ == '__main__':
    build()
