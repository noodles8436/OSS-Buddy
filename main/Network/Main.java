package oss;

import oss.Network;

public class Main {

	public static void main(String[] args) {
		Network network = Network.start();
		Network.login();
		Network.readyforLocation();
		Network.getBusList();
	}

}
