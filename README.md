# Homework 10 – User Authentication & Profile API

## Repository

- GitHub: [ykarthik03/homework10](https://github.com/ykarthik03/homework10)

## Closed Issues (with Documentation)

Below are links to the five resolved issues, each with test code, documentation, and application code changes:

1. **Username Validation**
   - [Issue #X: Username/Nickname Validation](https://github.com/ykarthik03/homework10/issues/X)
     - Enforced allowed characters, minimum length, and uniqueness for nicknames.
     - Added/updated tests for valid/invalid nicknames and uniqueness on update.

2. **Password Validation**
   - [Issue #Y: Password Complexity & Hashing](https://github.com/ykarthik03/homework10/issues/Y)
     - Enforced password complexity (length, case, digit, special char) and hashing.
     - Tests for weak/strong passwords and proper hashing.

3. **Profile Field Edge Cases**
   - [Issue #Z: Profile Field Edge Cases](https://github.com/ykarthik03/homework10/issues/Z)
     - Tested updating bio, profile picture, and URLs both individually and in combination.
     - Ensured API handles all combinations gracefully.

4. **Additional Edge Case/Access Control**
   - [Issue #A: Access Control & API Robustness](https://github.com/ykarthik03/homework10/issues/A)
     - Tested and fixed access control for user update/delete endpoints.
     - Added tests for unauthorized/forbidden access.

5. **Comprehensive Test Coverage**
   - [Issue #B: Test Coverage & Reliability](https://github.com/ykarthik03/homework10/issues/B)
     - Increased test coverage, added edge case tests, and improved reliability.

6. **Instructor Video Issue**
   - [Issue #C: (Describe the sixth issue here)](https://github.com/ykarthik03/homework10/issues/C)
     - *(You will fill this in after describing the sixth issue from the instructor video.)*

---

## Dockerhub Image

- [Dockerhub: ky253/homework10](https://hub.docker.com/r/ky253/homework10)

---

## Test Coverage

- **Coverage:** 83% (see `coverage.txt` for details)
- *(If you improve coverage to 90%+, update this section and add a badge or screenshot)*

---

## Reflection

This assignment deepened my understanding of robust API development and secure user authentication. I learned to enforce strict validation for usernames and passwords, ensuring both security and data integrity. Handling edge cases in profile updates and writing comprehensive tests helped me anticipate real-world usage scenarios and potential failures.

Collaboratively, I practiced using GitHub Issues, branching, and pull requests to track and document my work. This workflow not only improved code quality through review but also made my progress transparent and reproducible. The process of containerizing the app and pushing it to Dockerhub gave me practical DevOps experience. Overall, this assignment strengthened both my technical and collaborative skills.

---

## How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/ykarthik03/homework10.git
   cd homework10
   ```
2. Copy `.env.sample` to `.env` and fill in secrets.
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
4. Run tests:
   ```bash
   pytest --cov=app
   ```

---

## Links

- [Issues](https://github.com/ykarthik03/homework10/issues)
- [Pull Requests](https://github.com/ykarthik03/homework10/pulls)
- [Dockerhub Image](https://hub.docker.com/r/ky253/homework10)

---

## Notes

- Be sure to fill in the actual issue numbers/URLs.
- Add a screenshot or badge for coverage if possible.
- Fill in the sixth issue after you describe it.
