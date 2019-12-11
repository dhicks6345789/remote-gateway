package org.apache.guacamole.auth;

import java.net.URL;
import java.util.Map;
import java.util.HashMap;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.io.IOException;
import org.apache.guacamole.GuacamoleException;
import org.apache.guacamole.net.auth.simple.SimpleAuthenticationProvider;
import org.apache.guacamole.net.auth.Credentials;
import org.apache.guacamole.protocol.GuacamoleConfiguration;

/**
 * Authentication provider implementation for MyStart.Online.
 */
public class MystartAuthenticationProvider extends SimpleAuthenticationProvider {
	@Override
	public String getIdentifier() {
		return "mystart";
	}

	@Override
	public Map<String, GuacamoleConfiguration> getAuthorizedConfigurations(Credentials credentials) throws GuacamoleException {
		String domain = credentials.getUsername().split(":")[0];
		String username = credentials.getUsername().split(":")[0];
		String loginToken = credentials.getPassword();
		
		try {
			URL url = new URL("https://" + domain + "/api/confirmGuacamoleLoginToken?guacamoleLoginToken=" + loginToken);
			HttpURLConnection con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			int status = con.getResponseCode();
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String confirmedUsername = in.readLine();
			in.close();
		
			// If wrong username, fail.
			//if (!confirmedUsername.equals(username))
				//return null;
		
			// Successful login. Return configurations (STUB).
			return new HashMap<String, GuacamoleConfiguration>();
		} catch(IOException ex) {
        		return null;
		}
	}
}
