package com.svorah.testrepo;

import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

/** N-CRYPTO (Java half) | sanitiser layer 2 (crypto lib) | pairs P-JAVA | expected: 0 findings.
 *  Cipher.doFinal encrypts the PII before it reaches the print sink, clearing the flow. */
public class NCrypto {
    public void handle(User user) throws Exception {
        SecretKeySpec key = new SecretKeySpec(new byte[16], "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        byte[] encrypted = cipher.doFinal(user.getAadhaar().getBytes());
        System.out.println(Base64.getEncoder().encodeToString(encrypted));
    }
}
