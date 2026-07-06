import { initializeApp } from "https://www.gstatic.com/firebasejs/12.15.0/firebase-app.js";

import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/12.15.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyBWym2k-5BsHpj23tyZjFnLndk9Pem6VFE",

  authDomain: "cropcareai-969e9.firebaseapp.com",

  projectId: "cropcareai-969e9",

  storageBucket: "cropcareai-969e9.firebasestorage.app",

  messagingSenderId: "854023923140",

  appId: "1:854023923140:web:da4ed69b3f6bfda0dc7091",

  measurementId: "G-4T5FT7P8Q0",
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export const provider = new GoogleAuthProvider();

export { signInWithPopup, signOut, onAuthStateChanged };
