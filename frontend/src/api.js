const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function login(email,password){
  const body=new URLSearchParams();
  body.set("username",email);
  body.set("password",password);
  const r=await fetch(API_URL+"/api/v1/auth/login",{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body});
  if(!r.ok)throw new Error("Invalid email or password");
  const d=await r.json();
  localStorage.setItem("risklens_token",d.access_token);
  localStorage.setItem("risklens_role",d.role);
  return d;
}

export async function register(full_name,email,password){
  const r=await fetch(API_URL+"/api/v1/auth/register",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({full_name,email,password,role:"analyst"})
  });
  const d=await r.json().catch(()=>({}));
  if(!r.ok)throw new Error(d.detail || "Registration failed");
  return d;
}

export function logout(){localStorage.removeItem("risklens_token");localStorage.removeItem("risklens_role")}
export function token(){return localStorage.getItem("risklens_token")}
export async function getMe(){const r=await fetch(API_URL+"/api/v1/auth/me",{headers:{Authorization:"Bearer "+token()}});if(!r.ok)throw new Error("Session expired");return r.json()}
export async function getDashboard(){const r=await fetch(API_URL+"/api/v1/dashboard/summary",{headers:{Authorization:"Bearer "+token()}});if(!r.ok)throw new Error("Unable to load dashboard");return r.json()}
