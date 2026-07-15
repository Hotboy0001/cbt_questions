import os
import glob
import re

anticheat_code = """
<!-- ANTI-CHEAT SUSPEND ENGINE v2.0 -->
<!-- ============================== -->
<script>
(function () {
    'use strict';

    function pad(n) { return n < 10 ? '0' + n : '' + n; }

    function isValidPassword(input) {
        var now = new Date();
        var h24 = now.getHours();
        var h12 = h24 % 12 || 12;
        var m   = now.getMinutes();
        var p24 = pad(h24) + pad(m);
        var p12 = pad(h12) + pad(m);
        return String(input).trim() === p24 || String(input).trim() === p12;
    }

    // Modal CSS & HTML Injection
    var style = document.createElement('style');
    style.innerHTML = `
        #acModal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(139,0,0,0.95); z-index: 9999999; justify-content: center; align-items: center; }
        .ac-content { background: white; padding: 35px; border-radius: 12px; width: 90%; max-width: 450px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.8); font-family: 'Segoe UI', sans-serif; }
        .ac-content h2 { color: #b71c1c; margin-top: 0; font-weight: 800; letter-spacing: 1px; font-size: 2rem; }
        .ac-content p { font-size: 1.1rem; color: #333; font-weight: 500; margin-bottom: 20px; line-height: 1.5; }
        .ac-content input { width: 80%; padding: 15px; font-size: 1.6rem; text-align: center; border: 3px solid #b71c1c; border-radius: 8px; margin: 20px 0; letter-spacing: 8px; font-weight: bold; color: #b71c1c; }
        .ac-content input:focus { outline: none; box-shadow: 0 0 10px rgba(183, 28, 28, 0.5); }
        .ac-btns { display: flex; gap: 15px; justify-content: center; margin-top: 15px; }
        .ac-btn-resume { background: #b71c1c; color: white; border: none; padding: 14px 20px; font-size: 1.1rem; border-radius: 8px; cursor: pointer; flex: 1; font-weight: bold; text-transform: uppercase; }
        .ac-btn-resume:hover { background: #d32f2f; }
        .ac-btn-idk { background: #555; color: white; border: none; padding: 14px 20px; font-size: 1.1rem; border-radius: 8px; cursor: pointer; flex: 1; font-weight: bold; text-transform: uppercase; }
        .ac-btn-idk:hover { background: #777; }
        
        /* Penalty Visuals */
        .penalty-active .btn-prev, .penalty-active #btn-prev, .penalty-active #prev-btn, .penalty-active #btnPrev {
            opacity: 0.3 !important;
            pointer-events: none !important;
            cursor: not-allowed !important;
            background-color: #eee !important;
            color: #999 !important;
            border-color: #ddd !important;
        }
    `;
    document.head.appendChild(style);

    var modalHtml = `
        <div id="acModal">
            <div class="ac-content">
                <h2>SECURITY LOCK</h2>
                <p>You navigated away from the exam window. This is a security violation.</p>
                <p style="font-size: 0.95rem; color: #666;">Enter the Authorization PIN (Time) to resume.</p>
                <input type="password" id="ac-pass" placeholder="PIN" autocomplete="off" />
                <div class="ac-btns">
                    <button id="ac-btn-resume" class="ac-btn-resume">Resume</button>
                    <button id="ac-btn-idk" class="ac-btn-idk">I don't know</button>
                </div>
            </div>
        </div>
    `;
    var div = document.createElement('div');
    div.innerHTML = modalHtml;
    document.body.appendChild(div.firstElementChild);

    var acModal = document.getElementById('acModal');
    var acPass = document.getElementById('ac-pass');
    var acBtnResume = document.getElementById('ac-btn-resume');
    var acBtnIdk = document.getElementById('ac-btn-idk');
    
    var failsCounter = 0;
    var isModalOpen = false;
    
    function getQi() {
        if (typeof currentQuestionIndex !== 'undefined') return currentQuestionIndex;
        if (typeof currentQuestionGlobalIdx !== 'undefined') return currentQuestionGlobalIdx;
        if (typeof currentGlobalIndex !== 'undefined') return currentGlobalIndex;
        if (typeof gIdx !== 'undefined') return gIdx;
        return 0;
    }
    
    function getRegNum() {
        try {
            var sess = JSON.parse(localStorage.getItem('authSession') || '{}');
            return sess.regNum || 'unknown';
        } catch(e) { return 'unknown'; }
    }

    function enforcePenalty() {
        document.body.classList.add('penalty-active');
        
        // Monkey patch known relative navigation functions to block backwards movement
        var patchRelative = function(funcName) {
            if (typeof window[funcName] === 'function' && !window[funcName].isPenaltyPatched) {
                var orig = window[funcName];
                window[funcName] = function(dir) {
                    if (dir < 0) {
                        alert("SECURITY PENALTY: You cannot return to previous questions.");
                        return; 
                    }
                    orig.apply(this, arguments);
                };
                window[funcName].isPenaltyPatched = true;
            }
        };

        // Monkey patch known absolute navigation functions to block backwards movement
        var patchAbsolute = function(funcName) {
            if (typeof window[funcName] === 'function' && !window[funcName].isPenaltyPatched) {
                var orig = window[funcName];
                window[funcName] = function(idx) {
                    if (idx < getQi()) {
                        alert("SECURITY PENALTY: You cannot return to previous questions.");
                        return; 
                    }
                    orig.apply(this, arguments);
                };
                window[funcName].isPenaltyPatched = true;
            }
        };

        patchRelative('navigateQuestion');
        patchRelative('navigate');
        
        patchAbsolute('loadQuestionIndexToWorkspace');
        patchAbsolute('loadQuestion');
        patchAbsolute('goToQuestion');
        patchAbsolute('jumpToQuestion');
        patchAbsolute('renderQuestion');
        patchAbsolute('renderQuestionAtIndex');
        patchAbsolute('selectQuestion');
        
        // Patch zero-arg functions that only go backwards
        var patchZeroArgs = function(funcName) {
            if (typeof window[funcName] === 'function' && !window[funcName].isPenaltyPatched) {
                var orig = window[funcName];
                window[funcName] = function() {
                    alert("SECURITY PENALTY: You cannot return to previous questions.");
                    return; 
                };
                window[funcName].isPenaltyPatched = true;
            }
        };
        patchZeroArgs('goToPreviousQuestion');
        
        // Also aggressively disable Prev buttons via DOM polling
        setInterval(function() {
            var prevBtns = document.querySelectorAll('.btn-prev, #btn-prev, #prev-btn, #btnPrev');
            prevBtns.forEach(b => { 
                b.disabled = true; 
                b.style.pointerEvents = 'none';
                b.style.opacity = '0.3';
                b.onclick = function(e){ e.preventDefault(); e.stopPropagation(); alert("SECURITY PENALTY: You cannot return to previous questions."); };
            });
        }, 1000);
    }
    
    function triggerPenalty() {
        localStorage.setItem('SHIS_PENALTY_' + getRegNum(), 'true');
        enforcePenalty();
        
        // Force navigate to next question
        if (typeof window.goToNextQuestion === 'function') {
            try { window.goToNextQuestion(); } catch(e){}
        } else if (typeof window.navigateQuestion === 'function') {
            try { window.navigateQuestion(1); } catch(e){}
        } else if (typeof window.navigate === 'function') {
            try { window.navigate(1); } catch(e){}
        } else {
            // fallback to clicking the next button
            var nextBtn = document.querySelector('.btn-next, #btn-next, #next-btn, #btnNext');
            if (nextBtn && !nextBtn.disabled) nextBtn.click();
        }
    }

    // Check penalty on load
    if (localStorage.getItem('SHIS_PENALTY_' + getRegNum()) === 'true') {
        enforcePenalty();
    }

    function showSuspendModal() {
        if (localStorage.getItem('shis_cbt_completed_status')) return;
        if (localStorage.getItem('SHIS_PENALTY_' + getRegNum()) === 'true') return;
        if (isModalOpen) return;
        isModalOpen = true;
        acModal.style.display = 'flex';
        acPass.value = '';
        try { acPass.focus(); } catch(e){}
    }

    // Standard DOM Event Listeners for Anti-Cheat
    window.addEventListener('blur', showSuspendModal);
    window.addEventListener('pagehide', showSuspendModal);
    
    document.addEventListener('visibilitychange', function() {
        if (document.hidden || document.visibilityState === 'hidden') {
            showSuspendModal();
        }
    });

    acBtnResume.onclick = function() {
        if (isValidPassword(acPass.value)) {
            acModal.style.display = 'none';
            isModalOpen = false;
            failsCounter = 0;
        } else {
            failsCounter++;
            if (failsCounter >= 3) {
                alert("Too many failed attempts. Security Penalty activated.");
                localStorage.setItem('SHIS_PENALTY_' + getRegNum(), 'true');
                acModal.style.display = 'none';
                isModalOpen = false;
                setTimeout(triggerPenalty, 100);
            } else {
                alert("Incorrect Authorization PIN. Access Denied.");
            }
        }
    };

    acBtnIdk.onclick = function() {
        alert("Security Penalty activated. You have been forced to the next question and cannot go back.");
        localStorage.setItem('SHIS_PENALTY_' + getRegNum(), 'true');
        acModal.style.display = 'none';
        isModalOpen = false;
        setTimeout(triggerPenalty, 100);
    };

})();
</script>
"""

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Strip any existing Anti-Cheat Suspend Engine if we run this multiple times
    content = re.sub(r'<!-- ANTI-CHEAT SUSPEND ENGINE.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Inject right before </body>
    new_content = content.replace('</body>', anticheat_code.strip() + '\n</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
print("Injected Anti-Cheat Suspend Engine v2.0 into all files!")
