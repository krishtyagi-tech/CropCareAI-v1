import { auth, provider, signInWithPopup } from "./firebase-config.js";

export async function loginWithGoogle() {
  try {
    // --------------------------------------------------
    // Google Sign In
    // --------------------------------------------------

    const result = await signInWithPopup(auth, provider);

    const user = result.user;

    // --------------------------------------------------
    // Firebase ID Token
    // --------------------------------------------------

    const token = await user.getIdToken();

    // --------------------------------------------------
    // Verify Token with FastAPI
    // --------------------------------------------------

    const response = await fetch("http://127.0.0.1:8000/verify-token", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        token: token,
      }),
    });

    const verified = await response.json();

    if (!verified.success) {
      throw new Error("Token Verification Failed");
    }
    // await fetch("http://127.0.0.1:8000/session", {
    //   method: "POST",
    //   headers: {
    //     "Content-Type": "application/json",
    //   },
    //   body: JSON.stringify({
    //     uid: verified.uid,
    //     name: verified.name,
    //     email: verified.email,
    //   }),
    // });

    // --------------------------------------------------
    // Save Verified User
    // --------------------------------------------------

    localStorage.setItem(
      "cropcare_user",

      JSON.stringify({
        uid: verified.uid,

        name: verified.name,

        email: verified.email,

        token: token,

        photo: user.photoURL,

        loginTime: Date.now(),
      }),
    );

    console.log("Verified User");

    console.log(verified);

    return {
      uid: verified.uid,

      name: verified.name,

      email: verified.email,

      photo: user.photoURL,
    };
  } catch (error) {
    console.error(error);

    throw error;
  }
}
