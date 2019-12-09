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
		return "tutorial";
	}

	@Override
	public Map<String, GuacamoleConfiguration> getAuthorizedConfigurations(Credentials credentials) throws GuacamoleException {
		// Do nothing - yet.
		return null;
	}
}