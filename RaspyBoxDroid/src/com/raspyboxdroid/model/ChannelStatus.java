package com.raspyboxdroid.model;

public class ChannelStatus {
	
	private int status;
	
	public ChannelStatus(int id) {
		this.status = id;
	}
	
	public boolean isOn() {
		return this.status == 1;
	}
	
}
