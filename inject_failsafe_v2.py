import os
import glob
import re

failsafe_code = """
<!-- NETWORK FAILSAFE & RESUME ENGINE v1.2 -->
<!-- ===================================== -->
<script>
(function () {
    'use strict';

    function getSaveKey(regNum) {
        var fn = window.location.pathname.split('/').pop().replace(/\.html$/i, '');
        return 'SHIS_PROG_' + regNum + '_' + fn;
    }

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
        #resumeModal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 99999; justify-content: center; align-items: center; }
        .rm-content { background: white; padding: 30px; border-radius: 12px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); font-family: 'Segoe UI', sans-serif; }
        .rm-content h3 { color: #d32f2f; margin-top: 0; }
        .rm-content input { width: 80%; padding: 12px; font-size: 1.2rem; text-align: center; border: 2px solid #ccc; border-radius: 6px; margin: 15px 0; letter-spacing: 3px; }
        .rm-content button { background: #1976d2; color: white; border: none; padding: 12px 25px; font-size: 1.1rem; border-radius: 6px; cursor: pointer; width: 100%; }
        .rm-content button:hover { background: #1565c0; }
    `;
    document.head.appendChild(style);

    var modalHtml = `
        <div id="resumeModal">
            <div class="rm-content">
                <h3>CONNECTION LOST</h3>
                <p>The system detected a potential network drop. Do you want to resume where you left off?</p>
                <input type="password" id="rm-pass" placeholder="Enter PIN to Resume" autocomplete="off" />
                <button id="rm-btn">Resume Test</button>
            </div>
        </div>
    `;
    var div = document.createElement('div');
    div.innerHTML = modalHtml;
    document.body.appendChild(div.firstElementChild);

    // Answer Variables Aggregator
    function getAnsRef() {
        if (typeof studentAnswers !== 'undefined') return studentAnswers;
        if (typeof candidateAnswers !== 'undefined') return candidateAnswers;
        if (typeof studentResponses !== 'undefined') return studentResponses;
        if (typeof responses !== 'undefined') return responses;
        if (typeof registeredStudentAnswers !== 'undefined') return registeredStudentAnswers;
        if (typeof selectedAnswers !== 'undefined') return selectedAnswers;
        return null;
    }

    // Time Variables Aggregator
    function getTsec() {
        if (typeof totalExamSecondsLeft !== 'undefined') return totalExamSecondsLeft;
        if (typeof totalSecondsRemaining !== 'undefined') return totalSecondsRemaining;
        if (typeof timeRemaining !== 'undefined') return timeRemaining;
        if (typeof timeLeft !== 'undefined') return timeLeft;
        if (typeof countdownValue !== 'undefined') return countdownValue;
        if (typeof totalTimeSeconds !== 'undefined') return totalTimeSeconds;
        return null;
    }
    
    // Set Time Variable
    function setTsec(val) {
        if (typeof totalExamSecondsLeft !== 'undefined') totalExamSecondsLeft = val;
        else if (typeof totalSecondsRemaining !== 'undefined') totalSecondsRemaining = val;
        else if (typeof timeRemaining !== 'undefined') timeRemaining = val;
        else if (typeof timeLeft !== 'undefined') timeLeft = val;
        else if (typeof countdownValue !== 'undefined') countdownValue = val;
        else if (typeof totalTimeSeconds !== 'undefined') totalTimeSeconds = val;
    }

    function getQi() {
        if (typeof currentQuestionIndex !== 'undefined') return currentQuestionIndex;
        if (typeof currentQuestionGlobalIdx !== 'undefined') return currentQuestionGlobalIdx;
        if (typeof currentGlobalIndex !== 'undefined') return currentGlobalIndex;
        if (typeof gIdx !== 'undefined') return gIdx;
        return 0;
    }
    
    function setQi(val) {
        if (typeof currentQuestionIndex !== 'undefined') currentQuestionIndex = val;
        else if (typeof currentQuestionGlobalIdx !== 'undefined') currentQuestionGlobalIdx = val;
        else if (typeof currentGlobalIndex !== 'undefined') currentGlobalIndex = val;
        else if (typeof gIdx !== 'undefined') gIdx = val;
    }

    function getSi() {
        if (typeof currentSubjectIdx !== 'undefined') return currentSubjectIdx;
        if (typeof activeSubjectTab !== 'undefined') return activeSubjectTab;
        if (typeof currentSubjectIndex !== 'undefined') return currentSubjectIndex;
        return 0;
    }
    
    function setSi(val) {
        if (typeof currentSubjectIdx !== 'undefined') currentSubjectIdx = val;
        else if (typeof activeSubjectTab !== 'undefined') activeSubjectTab = val;
        else if (typeof currentSubjectIndex !== 'undefined') currentSubjectIndex = val;
    }

    function triggerRender() {
        try { 
            if (typeof renderCurrentQuestionCard === 'function') renderCurrentQuestionCard();
            else if (typeof renderActiveQuestionCard === 'function') renderActiveQuestionCard();
            else if (typeof renderQuestion === 'function') renderQuestion();
            else if (typeof loadQuestionIndexToWorkspace === 'function') loadQuestionIndexToWorkspace(getQi());
            else if (typeof renderActiveSubjectQuestion === 'function') renderActiveSubjectQuestion();
        } catch (e) {}
    }
    
    // Determine deep count (for nested objects like {english:{}, commerce:{}})
    function getAnsCount(obj) {
        if (!obj) return 0;
        let c = 0;
        // If it's an array, count non-null
        if (Array.isArray(obj)) {
            for(let i=0; i<obj.length; i++) { if(obj[i] !== null) c++; }
            return c;
        }
        // If it's a nested object (e.g. {english: {0:1}, commerce: {2:1}})
        for (let k in obj) {
            if (obj.hasOwnProperty(k)) {
                if (typeof obj[k] === 'object' && obj[k] !== null && !Array.isArray(obj[k])) {
                    c += Object.keys(obj[k]).length;
                } else if (obj[k] !== null) {
                    c++;
                }
            }
        }
        return c;
    }

    function _save() {
        try {
            var sess = JSON.parse(localStorage.getItem('authSession') || 'null');
            if (!sess || !sess.regNum) return;
            
            // Do not save if already submitted or locked
            if (localStorage.getItem('shis_cbt_completed_status') || localStorage.getItem('shis_submission_log_' + sess.regNum.toLowerCase()) || localStorage.getItem('CBT_LOCK_' + sess.regNum)) {
                localStorage.removeItem(getSaveKey(sess.regNum)); return;
            }
            
            var ans = getAnsRef();
            var count = getAnsCount(ans);
            
            if (count === 0) return; // don't save empty states
            
            localStorage.setItem(getSaveKey(sess.regNum), JSON.stringify({
                name: sess.name, regNum: sess.regNum,
                subjectGroup: sess.subjectGroup || '',
                answers: ans, tsec: getTsec(), qi: getQi(), si: getSi(),
                at: new Date().toISOString(),
                count: count
            }));
        } catch (e) {}
    }

    function _restore() {
        try {
            var sess = JSON.parse(localStorage.getItem('authSession') || 'null');
            if (!sess || !sess.regNum) return;
            var st = JSON.parse(localStorage.getItem(getSaveKey(sess.regNum)) || 'null');
            if (!st || !st.answers) return;
            
            var m = document.getElementById('resumeModal');
            var p = document.getElementById('rm-pass');
            var b = document.getElementById('rm-btn');
            
            m.style.display = 'flex';
            p.focus();
            
            b.onclick = function() {
                if (isValidPassword(p.value)) {
                    // Inject answers deep merge
                    var ansRef = getAnsRef();
                    if (ansRef) {
                        if (Array.isArray(ansRef)) {
                            // If array, just copy non-null values
                            if (Array.isArray(st.answers)) {
                                for(let i=0; i<st.answers.length; i++) {
                                    if(st.answers[i] !== null) ansRef[i] = st.answers[i];
                                }
                            } else {
                                // st.answers is object
                                Object.keys(st.answers).forEach(k => {
                                    if(st.answers[k] !== null) ansRef[parseInt(k)] = st.answers[k];
                                });
                            }
                        } else {
                            // Deep merge objects
                            for (var k in st.answers) {
                                if (st.answers.hasOwnProperty(k)) {
                                    if (typeof st.answers[k] === 'object' && st.answers[k] !== null) {
                                        if(!ansRef[k]) ansRef[k] = {};
                                        for(var inner in st.answers[k]) {
                                            ansRef[k][inner] = st.answers[k][inner];
                                        }
                                    } else {
                                        ansRef[k] = st.answers[k];
                                    }
                                }
                            }
                        }
                    }
                    
                    if (st.tsec !== null) setTsec(st.tsec);
                    if (st.qi !== null) setQi(st.qi);
                    if (st.si !== null) setSi(st.si);
                    
                    m.style.display = 'none';
                    triggerRender();
                } else {
                    alert('Incorrect password. Please verify the system time.');
                }
            };
        } catch (e) {}
    }

    // Bind timers
    setInterval(_save, 5000);
    setTimeout(_restore, 2000);
    
})();
</script>
</body>
</html>
"""

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    # Strip everything from the old failsafe comment to the end of the file
    new_content = re.sub(r'<!-- NETWORK FAILSAFE.*?</html>', failsafe_code.strip(), content, flags=re.DOTALL | re.IGNORECASE)
    
    with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
        f.write(new_content)
        
print("Updated all Failsafe injections with v1.2!")
