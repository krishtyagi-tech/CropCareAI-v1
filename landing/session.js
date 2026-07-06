import { auth, onAuthStateChanged } from "./firebase-config.js";

export function checkUserSession() {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log("Already Logged In");

      console.log(user);

      const savedUser = JSON.parse(localStorage.getItem("cropcare_user"));

      if (savedUser) {
        console.log("Verified User Found");

        console.log(savedUser);

        // Uncomment after everything is working
        // window.location.href = "http://localhost:8501";
      }
    } else {
      console.log("No User Logged In");

      localStorage.removeItem("cropcare_user");
    }
  });
}
