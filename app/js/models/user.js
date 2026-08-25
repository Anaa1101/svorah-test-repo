// Person entity for the JS half of the corpus. Defined in-repo (cross-file source).
export class User {
  constructor() {
    this.email = "";   // standard tier -> MEDIUM
    this.aadhaar = ""; // severe tier -> CRITICAL
  }
}

export function loadUser() {
  return new User();
}
