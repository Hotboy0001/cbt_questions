import os

def inject_webhook(html_content, target_url):
    injection_script = f"""
    <!-- SHIS Webhook Engine -->
    <script>
    (function() {{
        var WEBHOOK_URL = "{target_url}";
        var webhookFired = false;

        function sendDataToGoogleSheets() {{
            if (webhookFired) return;
            webhookFired = true;

            setTimeout(function() {{
                try {{
                    var authSession = JSON.parse(localStorage.getItem('authSession')) || {{}};
                    var regNum = authSession.regNum || localStorage.getItem('activeCandidateReg') || "Unknown";
                    var name = authSession.studentName || authSession.name || "Unknown";
                    var studentClass = authSession.studentClass || authSession.class || "Unknown";
                    var dept = authSession.dept || "Unknown";
                    
                    var score = "";
                    var scoreIds = ['resPercentage', 'res-total-pct', 'res-percentage', 'resAccPercent', 'res-grade', 'res-total-score', 'resGrandScore', 'resCitPercent', 'res-score'];
                    for (var i = 0; i < scoreIds.length; i++) {{
                        var el = document.getElementById(scoreIds[i]);
                        if (el && el.innerText.trim() !== '' && el.innerText.trim() !== '---') {{
                            score += el.innerText.trim() + " ";
                        }}
                    }}
                    if (!score) score = "Check Dashboard";

                    var payload = {{
                        name: name,
                        regNum: regNum,
                        studentClass: studentClass,
                        dept: dept,
                        examTitle: document.title,
                        score: score
                    }};

                    fetch(WEBHOOK_URL, {{
                        method: 'POST',
                        mode: 'no-cors', // Bypass CORS restrictions
                        headers: {{
                            'Content-Type': 'text/plain;charset=utf-8',
                        }},
                        body: JSON.stringify(payload)
                    }}).catch(e => console.error("Webhook Error", e));
                }} catch(e) {{
                    console.error("Webhook Extraction Error", e);
                }}
            }}, 500); // 500ms delay to allow DOM to render the final score text
        }}

        // Intercept localStorage.setItem to detect exactly when the exam is submitted
        var originalSetItem = localStorage.setItem;
        localStorage.setItem = function(key, value) {{
            originalSetItem.apply(this, arguments);
            if (key === 'shis_cbt_completed_status' && value === 'true') {{
                sendDataToGoogleSheets();
            }}
        }};
    }})();
    </script>
    """

    import re
    # Remove existing engine if present
    html_content = re.sub(r'<!-- SHIS Webhook Engine -->.*?</script>', '', html_content, flags=re.DOTALL)
    
    # Inject right before the closing body tag
    return html_content.replace("</body>", injection_script + "\\n    </body>")

directory = r"c:\Users\joema\myantigravity\cbt_questions"
target_url = "https://script.google.com/macros/s/AKfycby7DOc43VySe7s7dY8fF0hg4i3OFHUc_4-AKf5qxQRAgdoHbzLZzevTQ-LoY_TYJRhC/exec"

count = 0
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = inject_webhook(content, target_url)

        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Injected Webhook Engine into {filename}")
            count += 1

print(f"\\nInjected Webhook Engine into {count} files!")
