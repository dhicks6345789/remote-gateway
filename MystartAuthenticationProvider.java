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

	/**
	 * This code is mostly taken straight from the "custom authentication" tutorial example. Authentication is handled by a
	 * separate server, somewhere on the Internet, that authenticates the user via OAuth and decides what that user is
	  * authorised to connect to. It then passes a username, domain and login token to this authentication module. We check the
	   * login token is valid, get the associated connection configuration, and return that in the correct format to the
	   * Guacamole client for it to open the connection.
	 */
	@Override
	public Map<String, GuacamoleConfiguration> getAuthorizedConfigurations(Credentials credentials) throws GuacamoleException {
		// We pass the domain and login token in the "password" field.
		String username = credentials.getUsername();
		String domain = credentials.getPassword().split(":")[0];
		String loginToken = credentials.getPassword().split(":")[1];
		
		try {
			// Pass the login token to the authentication server for it to reply with a valid connection setup.
			URL url = new URL("https://" + domain + "/api/confirmGuacamoleLoginToken?guacamoleLoginToken=" + loginToken);
			HttpURLConnection con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			int status = con.getResponseCode();
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			HashMap<String, String> connectionDetails = new HashMap<String, String>();
			String connectionDetailLine = null;
			// If all worked okay above, read the configuration passed back line by line and store the details.
			while ((connectionDetailLine = in.readLine()) != null) {
				connectionDetails.put(connectionDetailLine.split(":")[0], connectionDetailLine.split(":")[1]);
			}
			in.close();
		
			// Check that the username passed back from the authentication server matches.
			if (!connectionDetails.get("username").equals(username))
				return null;
			
			// Create a new Guacamole configuration object, ready to pass back to the Guacamole client.
			Map<String, GuacamoleConfiguration> configs = new HashMap<String, GuacamoleConfiguration>();
			GuacamoleConfiguration config = new GuacamoleConfiguration();
			// Set the Guacamole configuration object up with the values passed back from the authentication server.
			// Values are mostly simply passed through as-is, but there's a couple of minor fiddles needed along the
			// way.
			for (String parameter : connectionDetails.keySet()) {
				if (parameter.equals("protocol")) {
					config.setProtocol(connectionDetails.get(parameter));
				} else if (parameter.equals("remoteUsername")) {
					config.setParameter("username", connectionDetails.get(parameter));
				} else if (!parameter.equals("username") && !parameter.equals("connectionTitle")) {
					config.setParameter(parameter, connectionDetails.get(parameter));
				}
			}
			configs.put(connectionDetails.get("connectionTitle"), config);
			return configs;
		} catch(IOException ex) {
        		return null;
		}
	}
}
