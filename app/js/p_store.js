// P-STORE | pii-in-storage | DPDP-025 | expected: MEDIUM (email).
import { User } from "./models/user.js";

export function persist(user) {
  localStorage.setItem("e", user.email);
}
