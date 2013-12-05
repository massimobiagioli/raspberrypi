package com.raspyboxdroid;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;


public class RaspyBoxWsClient {
	
	private static final String URL_STATUS = "status";
	private static final String URL_POWERON = "poweron";
	private static final String URL_POWEROFF = "poweroff";
	
	private static final String API_MODEL_RELAY = "relay";
	
	private String address;
	private int port;
	
	private AsyncHttpClient client;
	
	public RaspyBoxWsClient() {
		this.client = new AsyncHttpClient();
	}
	
	public void listRelay(AsyncHttpResponseHandler responseHandler) {
		client.get(this.getEndpointApi(API_MODEL_RELAY), responseHandler);
	}
	
	public void status(int channel, AsyncHttpResponseHandler responseHandler) {
		client.get(this.getEndpointAction(URL_STATUS, channel), responseHandler);
	}
	
	public void powerOn(int channel, AsyncHttpResponseHandler responseHandler) {
		client.get(this.getEndpointAction(URL_POWERON, channel), responseHandler);
	}

	public void powerOff(int channel, AsyncHttpResponseHandler responseHandler) {
		client.get(this.getEndpointAction(URL_POWEROFF, channel), responseHandler);
	}	
	
	private String getEndpointAction(String call, int channel) {
		StringBuilder sb = new StringBuilder();
		sb.append("http://")
			.append(this.address)
			.append(":")
			.append(String.valueOf(this.port))
			.append("/")
			.append(call)
			.append("/")
			.append(String.valueOf(channel));
		
		return sb.toString();		
	}
	
	private String getEndpointApi(String model) {
		StringBuilder sb = new StringBuilder();
		sb.append("http://")
			.append(this.address)
			.append(":")
			.append(String.valueOf(this.port))
			.append("/api/")
			.append(model);
		
		return sb.toString();		
	}
	
	public String getAddress() {
		return address;
	}

	public void setAddress(String address) {
		this.address = address;
	}
	
	public int getPort() {
		return port;
	}

	public void setPort(int port) {
		this.port = port;
	}
	
}
