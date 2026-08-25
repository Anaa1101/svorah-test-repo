package com.svorah.testrepo;

/** Person entity for the Java half. Defined in-repo so Joern resolves the getters. */
public class User {
    private String aadhaar;   // severe tier -> CRITICAL
    private String password;  // severe tier -> CRITICAL

    public String getAadhaar() {
        return aadhaar;
    }

    public void setAadhaar(String aadhaar) {
        this.aadhaar = aadhaar;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
