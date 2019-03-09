package com.example.pritishsehzpaul.makeathon;

import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.button.MaterialButton;
import android.support.design.widget.TextInputEditText;
import android.support.v7.app.AppCompatActivity;
import android.util.JsonReader;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONException;

/**
 * A login screen that offers login via email/password.
 */
public class MainActivity extends AppCompatActivity {

    /**
     * Id to identity READ_CONTACTS permission request.
     */
    private static final int REQUEST_READ_CONTACTS = 0;

    /**
     * A dummy authentication store containing known user names and passwords.
     * TODO: remove after connecting to a real authentication system.
     */
    private static final String[] DUMMY_CREDENTIALS = new String[]{
            "foo@example.com:hello", "bar@example.com:world"
    };
    /**
     * Keep track of the login task to ensure we can cancel it if requested.
     */
    private GetUrlContentTask mAuthTask = null;

    // UI references.
    private TextInputEditText requestNameEdit;
    private TextInputEditText requestEmailEdit;
    private TextInputEditText requestContactEdit;
    private MaterialButton requestButton;
    private TextView deviceId;
    private TextView deviceName;
    private View mRequestAmbulanceForm;
    private View mProgressView;
    private String name, email, contact, response;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        // Set up the login form.
        requestNameEdit = (TextInputEditText) findViewById(R.id.name_request_edit_text);
        requestEmailEdit = (TextInputEditText) findViewById(R.id.email_request_edit_text);
        requestContactEdit = (TextInputEditText) findViewById(R.id.contact_request_edit_text);
        try {
            name = URLEncoder.encode(requestNameEdit.getText().toString(), "UTF-8");
            email = URLEncoder.encode(requestEmailEdit.getText().toString(), "UTF-8");
            contact = URLEncoder.encode(requestContactEdit.getText().toString(), "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }

        MaterialButton mRequestButton = (MaterialButton) findViewById(R.id.request_button);
        mRequestButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                String url = "http://ps-makeathon.herokuapp.com/v1/user/request?name=" + name + "&email=" + email
                        + "&contact=" + contact;
                new GetUrlContentTask().execute(url);
            }
        });

        mRequestAmbulanceForm = findViewById(R.id.request_ambulance_form);
        mProgressView = findViewById(R.id.request_progress);
    }

    private boolean isEmailValid(String email) {
        //TODO: Replace this with your own logic
        return email.contains("@");
    }

    private boolean isPasswordValid(String password) {
        //TODO: Replace this with your own logic
        return password.length() > 4;
    }

    void displayMessage(String result) {

        String id="Error in getting data",name="Error in getting data";
        try{
            System.out.println(response.toString());
            JSONObject jsonObj = new JSONObject(response);
            id = jsonObj.getString("device_id");
            name = jsonObj.getString("device_name");
        }
        catch(JSONException e){
            e.printStackTrace();
            id = "Error in parsing data";
            name = "Error in parsing data";
        }

        deviceId.setText(id);
        deviceId.setVisibility(View.VISIBLE);
        deviceName.setText(name);
        deviceName.setVisibility(View.VISIBLE);
    }

    /**
     * Represents an asynchronous login/registration task used to authenticate
     * the user.
     */
    public class GetUrlContentTask extends AsyncTask<String, Integer, String> {

        @Override
        protected String doInBackground(String... u) {
            try {
                URL url = new URL(u[0]);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                connection.setRequestMethod("GET");
                connection.setDoOutput(true);
                connection.setConnectTimeout(25000);
                connection.setReadTimeout(25000);
                connection.connect();
                BufferedReader rd = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                response = "";
                String line;
                System.out.println("Response received");
                while ((line = rd.readLine()) != null) {
                    response += line + "\n";
                    System.out.println(response);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
            return response;
        }

        protected void onProgressUpdate(Integer... progress) {
        }

        @Override
        protected void onPostExecute(String result) {
            // this is executed on the main thread after the process is over
            // update your UI here
            displayMessage(result);
        }
    }
}

