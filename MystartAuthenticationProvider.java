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
		String username = credentials.getUsername();
		String domain = credentials.getPassword().split(":")[0];
		String loginToken = credentials.getPassword().split(":")[1];
		
		try {
			URL url = new URL("https://" + domain + "/api/confirmGuacamoleLoginToken?guacamoleLoginToken=" + loginToken);
			HttpURLConnection con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			int status = con.getResponseCode();
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			HashMap<String, String> connectionDetails = new HashMap<String, String>();
			while ((connectionDetailLine = in.readLine()) != null) {
				connectionDetails.put(connectionDetailLine.split(":")[0], connectionDetailLine.split(":")[1]);
			}
			in.close();
		
			// If wrong username, fail.
			if (!connectionDetails("username").equals(username))
				return null;
			
			Map<String, GuacamoleConfiguration> configs = new HashMap<String, GuacamoleConfiguration>();
			
			// Create new configuration.
			GuacamoleConfiguration config = new GuacamoleConfiguration();
			
			// Set protocol
			for(Map.Entry<String, HashMap> entry : connectionDetails.entrySet()) {
				String parameter = entry.getKey();
				HashMap value = entry.getValue();
				if (parameter.equals("protocol")) {
					config.setProtocol(value);
				} else if (parameter.equals("remoteUsername")) {
					config.setParameter("username", value);
				} else if (!parameter.equals("username")) {
					config.setParameter(parameter, value);
				}
			}
			
			configs.put("MyStart Connection", config);
			return configs;
		} catch(IOException ex) {
        		return null;
		}
	}
}
