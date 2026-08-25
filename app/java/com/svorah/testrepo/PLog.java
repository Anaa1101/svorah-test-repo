package com.svorah.testrepo;

/** P-JAVA | pii-in-log (Java) | DPDP-002 | expected: CRITICAL (aadhaar). */
public class PLog {
    public void handle(User user) {
        System.out.println(user.getAadhaar());
    }
}
