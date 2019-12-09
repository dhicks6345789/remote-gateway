package org.apache.guacamole.auth;

import java.util.Map;
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
		// Get the Guacamole server environment
		//Environment environment = new LocalEnvironment();
		
		// If wrong username, fail
		if (!"bananas".equals(credentials.getUsername()))
			return null;
		
		// Successful login. Return configurations (STUB)
		return new HashMap<String, GuacamoleConfiguration>();
	}
}
