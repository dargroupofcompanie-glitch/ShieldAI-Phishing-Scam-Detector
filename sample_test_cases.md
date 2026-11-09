# Suggested test cases

Use fictional examples only. Do not paste real personal or banking messages.

| Input | Expected behaviour |
|---|---|
| "Your account is suspended. Verify now with your password." | High-risk signals for urgency and credentials |
| "Congratulations, claim your prize by paying a processing fee." | Payment/prize warning |
| "Hi, the class is moved to 10 AM tomorrow." | Likely low score |
| `http://192.0.2.10/login` | Flags non-HTTPS and IP-address host |
| `https://bit.ly/example` | Flags URL shortener |
| `https://www.example.com` | Few basic URL warning signs; not certified safe |

The IP address above is from a documentation-only range and is not a real service.
