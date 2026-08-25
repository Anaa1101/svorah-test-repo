// FP-READ | localStorage.getItem is a read, not a sink -> must not fire.
export function readEmailKey() {
  return localStorage.getItem("email");
}
