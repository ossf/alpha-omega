# Functionality Tests:
**1. Sending correct data to the Triage Portal using the POST API endpoint** 

**Preconditions:**

- Users must have valid credentials to access the API endpoint.
- The Triage Portal API endpoint URL and required payload structure are known.

**Steps to Test:**

- Obtain valid authentication credentials for the Triage Portal API.
- Set up the requested payload with the necessary data fields for the Triage Portal.
- Use an API testing tool to send a POST request to the Triage Portal API endpoint, providing the appropriate authentication credentials and payload.
- Capture and inspect the response from the API endpoint.
- Validate the response status code to ensure a successful request (200 OK).

**Expected Result:**

- The API request is successful, indicated by a response status code of 200.
- The Triage Portal processes sent data correctly, as indicated by any expected responses in the response body or headers.
- Any additional expected behaviors or validations specific to the Triage Portal API are met.

****

**2. Store parsed scan results from SARIF file into the findings table**

**Preconditions:**

- The API endpoint for receiving the SARIF file is available.
- Access to the database is established.

**Steps to Test:**

- Prepare a SARIF file with sample data to be sent through the API.
- Send an API request with the necessary data fields for the Triage Portal.
- Validate that the API successfully receives the SARIF file and extracts the relevant data from it.
- Store the extracted scan results data into the findings table of the database, ensuring proper mapping of the data fields.
- Compare the retrieved data with the original data from the SARIF file to ensure accurate storage and mapping.

**Expected Result:**

- The API should successfully receive the SARIF file without any errors.
- The SARIF file should be parsed, and the relevant data should be extracted and stored in the findings table accurately.

****

**3. Checking that it is a SARIF file when using the API endpoint**

**Preconditions:**

- The user has valid authentication credentials to access the API endpoint.
- The Triage Portal API endpoint URL is known.

**Steps to Test:**

- Obtain valid authentication credentials for the Triage Portal API.
- Prepare a non-SARIF file (e.g., text file, image file) to be sent through the API for testing.
- Send a POST request to the Triage Portal API endpoint, including the non-SARIF file in the request payload.
- Validate that the API endpoint enforces strict file type validation for the SARIF file field.
- Verify that the API rejects the request and returns an appropriate error response indicating that only SARIF files are allowed.
- Confirm that the error response contains clear and accurate information about the file type restriction.

**Expected Result:**

- When attempting to send a POST request with a non-SARIF file, the API should reject the request.

# Unit test cases:
**1. Verify that the API returns a 200 response when making a correct request**

    class TestPostAPI(unittest.TestCase):
        def setUp(self):
            # Set up any necessary data or configurations before each test case
            self.api_url = "http://example.com/api"  # Replace with actual API endpoint
    
        def test_post_request_returns_200(self):
            # Test that the POST request returns a 200 response
            file_path = "path/to/file.sarif"  # Replace with the actual path to the file
            files = {
                'file': open(file_path, 'rb')
            }
    
            payload = {
                "package_name": "my_package",
                "checksum": "abcd1234"
            }
            response = requests.post(self.api_url, files=files, data=payload)
            self.assertEqual(response.status_code, 200)

**2. Verify that the API returns an error response when making a wrong request**

    class TestPostAPI(unittest.TestCase):
        def setUp(self):
            # Set up any necessary data or configurations before each test case
            self.api_url = "http://example.com/api"  # Replace with actual API endpoint
    
        def test_post_request_returns_error_for_non_sarif_file(self):
            # Test that the POST request returns a 200 response
            file_path = "path/to/non_sarif_file.txt"  # Replace with the actual path to the file                                      
            files = {
                'file': open(file_path, 'rb')
            }
            payload = {
                "package_name": "my_package",
                "checksum": "abcd1234"
            }
            response = requests.post(self.api_url, files=files, data=payload)
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json())

# User-Interface Tests:
**1. Successful SARIF File Upload Notification**

**Preconditions:**

- The user is signed into the portal.
- The user is on the SARIF file upload page.
- The user has a valid SARIF file ready for upload.

**Steps to Test:**

- Choose the file to upload.
- Enter the package name in the designated input field.
- Click on the "Add" button.
- Wait for the upload process to complete.
- Observe the page for the presence of a successful notification.

**Expected Results:**

- The SARIF file should be uploaded successfully without any errors.
- A notification should be displayed to inform the user about the successful upload.

****

**2. The Wiki page UI separates the articles into unresolved (New, Not specified, Active) and resolved (Closed, Resolved)**

**Preconditions:**

- The user is logged into the portal.
- The user has appropriate permissions to add and view wiki articles.

**Steps to Test:**

- Navigate to the wiki page by clicking on the wiki tab.
- Fill in the required fields for creating an article, and on the “State” field choose either Closed or Resolved.
- Click on the "Add" button to add the article.
- Click on the "View All" button to view the list of wiki articles.
- Verify that the article created is not listed in the "Unresolved Wiki Articles" table.
- Locate the "Resolved Wiki Articles" section.
- Click on the arrow next to the "Resolved Wiki Articles" title to expand the table.** 
- Verify that the article created is listed in the " Resolved Wiki Articles" table.

**Expected Result:**

- The resolved or closed article should be displayed under the "Resolved Wiki Articles" table when the corresponding state is selected.


# Security test case:
**1. Authorization and Access Control for Sending SARIF File Information**

**Preconditions:**

- The Triage Portal API endpoint URL and required payload structure are known.
- User authentication and authorization mechanisms are in place.

**Steps to Test:**

- Attempt to send a POST request to the Triage Portal API endpoint without authentication or with invalid credentials, including SARIF file information in the request payload.
- Verify that the API rejects the request and returns an appropriate unauthorized or forbidden response.
- Use valid authentication credentials for a non-authorized user (e.g., a user without proper privileges or role) to send a POST request with SARIF file information to the API endpoint.
- Verify that the API rejects the request and returns an appropriate unauthorized or forbidden response.
- Use valid authentication credentials for an authorized user to send a POST request with SARIF file information to the API endpoint.
- Verify that the API accepts the request and returns a successful response, indicating that the SARIF file information has been sent to the Triage Portal successfully.

**Expected Result:**

- Access control mechanisms should be properly enforced, and unauthorized or non-privileged users should be denied access to the API endpoint.
# Integration test cases:
**1. Verify that the Analyzer can successfully upload SARIF File to Triage Portal through the API Endpoint**

**Preconditions:**

- The Analyzer and Triage Portal applications are installed and running.
- The API endpoint for sending data from the Analyzer to the Triage Portal is properly implemented and accessible.
- The Analyzer application has valid authentication credentials to access the Triage Portal API.

**Steps to Test:**

- Open the Analyzer application and push the necessary information to the Triage Portal.
- Ensure that the Analyzer application invokes the API endpoint to send the data to the Triage Portal.
- Monitor the network traffic or API logs to confirm that the data is sent to the correct API endpoint.

**Expected Results:**

- The Analyzer application successfully sends the data to the Triage Portal API endpoint.

****

**2. Verify that the Triage Portal correctly stores the data received from the Analyzer – Assertion Data Available.**

**Preconditions:**

- The Analyzer and Triage Portal applications are installed and running.
- The API endpoint for sending data from the Analyzer to the Triage Portal is properly implemented and accessible.
- The Analyzer application has valid authentication credentials to access the Triage Portal API.

**Steps to Test:**

- Open the Analyzer application and push the necessary information to the Triage Portal with assertion data available.
- Access the Triage Portal’s corresponding database.
- Verify that the parse assertion report is properly stored in the assertion table, including all relevant details and attributes.
- Verify that the parse scan results are properly stored in the findings table, including all relevant details and attributes.
- Validate the data integrity by comparing key fields between the sent data and the stored data in the Triage Portal.

**Expected Results:**

- The Triage Portal application correctly receives and saves the data sent from the Analyzer.

****

**3. Verify that the Triage Portal correctly stores the data received from the Analyzer – No Assertion Data Available.**

**Preconditions:**

- The Analyzer and Triage Portal applications are installed and running.
- The API endpoint for sending data from the Analyzer to the Triage Portal is properly implemented and accessible.
- The Analyzer application has valid authentication credentials to access the Triage Portal API.

**Steps to Test:**

- Open the Analyzer application and push the necessary information to the Triage Portal with no assertion data available.
- Access the Triage Portal’s corresponding database.
- Verify the data is properly stored in the findings table, including all relevant details and attributes.
- Validate the data integrity by comparing key fields between the sent data and the stored data in the Triage Portal.
- Verify nothing was stored in the assertion table.

**Expected Results:**

- The Triage Portal application correctly receives and saves the data sent from the Analyzer.

****

**4. Analyzer to Triage Portal scalability when processing large data sets or high data volumes.**

**Preconditions:**

- The Analyzer and Triage Portal applications are installed and running.
- The API endpoint for sending data from the Analyzer to the Triage Portal is properly implemented and accessible.
- The Analyzer application has valid authentication credentials to access the Triage Portal API.

**Steps to Test:**

- Open the Analyzer application and push the necessary information to the Triage Portal.
- Repeat the above step multiple times for pushing data to the Triage Portal. Make sure to include large/heavy files.
- Monitor the performance, response times, or API logs of both the Analyzer and Triage Portal during the data integration.
- Verify that the integration remains stable, and the response times are within acceptable limits.
- Verify that the data is consistently and accurately saved in the Triage Portal.

**Expected Results:**

- The integration between the Analyzer and Triage Portal remains stable and performs well, even with large data sets or high data volumes.

****

**5. Unauthenticated User Data Submission Integration Test**

**Preconditions:**

- The Analyzer application does not have valid authentication credentials to access the Triage Portal API.
- The Analyzer and Triage Portal applications are installed and running.
- The API endpoint for sending data from the Analyzer to the Triage Portal is properly implemented and accessible.

**Steps to Test:**

- Open the Analyzer application and push the necessary information to the Triage Portal.
- Monitor the network traffic or API logs to confirm that the data submission request is made to the Triage Portal API endpoint.
- Verify that the Triage Portal returns an appropriate error response indicating unauthorized access.

**Expected Results:**

- The Triage Portal rejects the data submission request and returns an appropriate error response indicating unauthorized access.

