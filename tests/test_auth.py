def test_login_incorrect_password():
  """Test login with incorrect password"""
  # Create a user and test login with incorrect password.
  # Expected output: Login failed error, redirect back to login page

def test_login_correct_password():
  """Test login with correct password"""
  # Create a user and test login with correct password.
  # Expected output: Login successful, redirect to home page

def test_csrf_token_missing_login():
  """Test login form submission without CSRF token"""
  # Create post request to login endpoint from outside the
  # application (i.e., without CSRF token). 
  # Expected output: status code 400 error
  
def test_csrf_token_present_login():
  """Test login form submission with CSRF token"""
  # Create a user and log in through the application to test
  # CSRF token is generated and included in the form. 
  # Expected output: Login successful, redirect to home page

def test_csrf_token_missing_signup():
  """Test signup form submission without CSRF token"""
  # Create post request to signup endpoint from outside the
  # application (i.e., without CSRF token).
  # Expected output: status code 400 error

def test_csrf_token_present_signup():
  """Test signup form submission with CSRF token"""
  # Create a user through the application to test
  # CSRF token is generated and included in the form.
  # Expected output: Sign up successful

def test_signup_password_hashing():
  """Test password hashing during signup"""
  # Create a user and check that the passwords are hashed.
  # Expected output: Password is hashed in database

def test_logout_terminates_session():
  """Test logout terminates session data"""
  # Check session data to make sure logging out kills session cookie.
  # Expected output: Session data is cleared after logout.

def test_sql_injection_login():
  """Test SQL injection vulnerability in login"""
  # Attempt to inject malicious SQL code in login form.
  # Expected output: Login failed error, redirect back to login page

def test_sql_injection_signup():
  """Test SQL injection vulnerability in signup"""
  # Attempt to inject malicious SQL code in signup form.
  # Expected output: Sign up failed error, redirect back to signup page

def test_xss_vulnerability_login():
  """Test XSS vulnerability in login"""
  # Attempt to inject malicious JavaScript code in login form.
  # Expected output: Login failed error, redirect back to login page

def test_xss_vulnerability_signup():
  """Test XSS vulnerability in signup"""
  # Attempt to inject malicious JavaScript code in signup form.
  # Expected output: Sign up failed error, redirect back to signup page