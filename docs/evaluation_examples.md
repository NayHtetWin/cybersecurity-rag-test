## Evaluation Examples

### Question 1

**Q:** Tell me about Mitigation Object Structure

**A:** The Mitigation Object Structure describes the categories or classes of technologies used as mitigations in the context of cybersecurity, which are vendor product agnostic and focus on general methods rather than specific solutions. These objects are structured similarly to techniques and sub-techniques, groups, and software. Each mitigation object can be annotated with tags for filtering and pivoting purposes, and includes free text fields to detail the specifics of how a mitigation can apply to a given (sub-)technique.

For instance, mitigations like Application Isolation and Sandboxing, Data Backup, Execution Prevention, and Network Segmentation are categorized under this structure. These categories help in understanding the types of technologies that can mitigate specific techniques or sub-techniques used by cyber adversaries [Source: ../dataset/mitre-attack-philosophy-2020.pdf, Page: 26].

The structure allows for detailed documentation on how these mitigations relate to particular (sub-)techniques, providing information necessary for network defenders and policymakers to implement appropriate measures. This approach was introduced in ATT&CK for Mobile first and later adopted by ATT&CK for Enterprise after a July 2019 update [Source: ../dataset/mitre-attack-philosophy-2020.pdf, Page: 26].

---

### Question 2

**Q:** What are Penetration Testing: Pentest according to Thailand Web Security Standard?

**A:** According to the Thailand Web Security Standard 2025, Penetration Testing: Pentest (Penetration Testing) is described as follows:

Penetration Testing: Pentest (`Penetration Testing`) involves assessing the security of a website by simulating malicious activities to identify vulnerabilities. Specifically, it includes testing for `SQL Injection`, `Cross-Site Scripting (XSS)`, and `User Impersonation`. [Source: ../dataset/thailand-web-security-standard-2025.pdf, Page: 31]

---

### Question 3

**Q:** Give me example of Broken Access Control

**A:** Sure, here are some examples of broken access control:

- Bypassing access control checks by modifying the URL (parameter tampering or force browsing), internal application state, or the HTML page. [Source: ../dataset/owasp-top-10.pdf, Page: 8]
- Permitting viewing or editing someone else's account, by providing its unique identifier (insecure direct object references). [Source: ../dataset/owasp-top-10.pdf, Page: 8]
- Accessing API with missing access controls for POST, PUT and DELETE. [Source: ../dataset/owasp-top-10.pdf, Page: 8]
- Elevation of privilege; acting as a user without being logged in or acting as an admin when logged in as a user. [Source: ../dataset/owasp-top-10.pdf, Page: 8]

---

### Question 4

**Q:** How does MITRE describe the purpose of Persistence techniques?

**A:** Based on the provided context, MITRE describes Persistence as a tactic that involves techniques to maintain access over an extended period. The context mentions specific sub-techniques related to Persistence such as Pre-OS Boot, Account Manipulation, Scheduled Task/Job, and Server Software Component [Source: ../dataset/mitre-attack-philosophy-2020.pdf, Page: 16].

However, the exact purpose of Persistence techniques is not explicitly stated within the given excerpts. Therefore, I cannot provide a specific purpose based solely on the information provided.

If you need more detailed information about the purpose of Persistence techniques in MITRE's framework, additional context or documents may be required. [Source: ../dataset/mitre-attack-philosophy-2020.pdf, Page: 16]

---

## Limitations

- Cannot detect relevant answers when the question or context is too vague. For example, "Tell me about Datasets in OWASP Top 10" fails to return an answer.
- To avoid over-engineering, re-ranking and hybrid search were not implemented.
- For simplicity, context control relies solely on strict prompt engineering without additional guardrails.
- Since the Thailand Web Security Standard is in Thai, no explicit Thai language handling was implemented. Qwen 2.5 handles multilingual content automatically.

*Example of limitation:*

**Q:** Tell me about Data Factors from OWASP Top 10.

**A:** I cannot answer this based on the provided documents. The context does not contain any specific information about "Data Factors" from OWASP Top 10. It primarily discusses the overview of OWASP, the structure and use cases of the OWASP Top 10: 2021, and its application as a standard for various security practices.
