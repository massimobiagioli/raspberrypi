package com.raspyboxdroid;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.TextView;
import android.widget.ToggleButton;

import com.google.gson.Gson;
import com.google.gson.internal.LinkedTreeMap;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.raspyboxdroid.model.ChannelStatus;
import com.raspyboxdroid.model.Relay;

public class MainActivity extends Activity {
    
	private static final String LOG_TAG = "RASPYBOXDROID";
	
	private static final String DEFAULT_IP_ADDRESS = "10.0.2.2";	// Emulator Host IP
	private static final String DEFAULT_PORT = "80";
	
	private static final String KEY_IP_ADDRESS = "ip_address";
	private static final String KEY_PORT = "port";
	
	private RaspyBoxWsClient raspyBoxWsClient;	
	private Map<String, Integer> buttonMap;
	private Map<String, Integer> labelMap;
	private List<Relay> relays;
	
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);        
        setContentView(R.layout.activity_main);      
        this.initLabelMap();
        this.initButtonMap();        
        this.initClient();
    }

    public boolean onCreateOptionsMenu(Menu menu) {        
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
		
	public boolean onOptionsItemSelected(MenuItem item) {		
		switch (item.getItemId()) {
		case R.id.action_settings:
			showSettings();
			break;
		}		
		return super.onOptionsItemSelected(item);
	}	
				
	protected void onResume() {
		super.onResume();
		this.setRaspberryIPAddress();
	}

	private void showSettings() {
		Intent intent = new Intent(MainActivity.this, SettingsActivity.class);
		startActivity(intent);
	}	
	
	private void setRaspberryIPAddress() {
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);		
		TextView label = ((TextView)findViewById(R.id.lblIpAddress));
		String ip = prefs.getString(KEY_IP_ADDRESS, null);
		if (null != ip) {
			label.setText(this.getString(R.string.raspberrypi_address) + " : " + ip);	
		} else {
			label.setText(this.getString(R.string.raspberrypi_missing_address));
		}				
	}
	
	private void initClient() {
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
		this.raspyBoxWsClient = new RaspyBoxWsClient();
		this.raspyBoxWsClient.setAddress(prefs.getString(KEY_IP_ADDRESS, DEFAULT_IP_ADDRESS));
		this.raspyBoxWsClient.setPort(Integer.valueOf(prefs.getString(KEY_PORT, DEFAULT_PORT)));						
		this.raspyBoxWsClient.listRelay(new AsyncHttpResponseHandler() {
			public void onSuccess(String response) {
				populateRelaysFromJson(response);
				initRelayControls();
			}
			public void onFailure(Throwable t, String e) {
				Log.d(LOG_TAG, e);
			}
		});
	}
	
	private void initRelayControls() {
		this.resetRelayControls();		
		 
		for (final Relay relay : relays) {
			this.raspyBoxWsClient.status(relay.getChannel(), new AsyncHttpResponseHandler() {
				public void onSuccess(String response) {
					ChannelStatus channelStatus = new ChannelStatus(exitCodeFromJson(response));
					initLabel(labelMap.get(String.valueOf(relay.getChannel())), relay.getChannel(), relay);
					initButton(buttonMap.get(String.valueOf(relay.getChannel())), relay.getChannel(), channelStatus); 
				}
				public void onFailure(Throwable t, String e) {
					Log.d(LOG_TAG, e);
				}
			});
		}				
	}
	
	private void resetRelayControls() {
		for (int i = 1; i <= 4; i++) {
			TextView label = (TextView) findViewById(labelMap.get(String.valueOf(i)));
			label.setVisibility(4);
			ToggleButton button = (ToggleButton) findViewById(buttonMap.get(String.valueOf(i)));
			button.setVisibility(4);
		}
	}
	
	private void initLabel(int labelId, final int channel, Relay relay) {
		TextView label = (TextView) findViewById(labelId);
		label.setVisibility(0);
		label.setText(relay.getDevice());
	}
	
	private void initButton(int buttonId, final int channel, final ChannelStatus channelStatus) {
		final ToggleButton button = (ToggleButton) findViewById(buttonId);		
		button.setVisibility(0);
		button.setChecked(channelStatus.isOn());
		button.setOnClickListener(new OnClickListener() {						
			public void onClick(View v) {
				if (button.isChecked()) {
					raspyBoxWsClient.powerOn(channel, new AsyncHttpResponseHandler() {
						public void onSuccess(String response) {
							ChannelStatus channelStatus = new ChannelStatus(exitCodeFromJson(response));
							button.setChecked(channelStatus.isOn());
						}
						public void onFailure(Throwable t, String e) {
							Log.d(LOG_TAG, e);
						}
					});		
				} else {
					raspyBoxWsClient.powerOff(channel, new AsyncHttpResponseHandler() {
						public void onSuccess(String response) {
							ChannelStatus channelStatus = new ChannelStatus(exitCodeFromJson(response));
							button.setChecked(channelStatus.isOn());
						}
						public void onFailure(Throwable t, String e) {
							Log.d(LOG_TAG, e);
						}
					});		
				}						
			}
		});		
	}
	
	private void initButtonMap() {
		buttonMap = new HashMap<String, Integer>();
		buttonMap.put("1", R.id.tglDevice1);
		buttonMap.put("2", R.id.tglDevice2);
		buttonMap.put("3", R.id.tglDevice3);
		buttonMap.put("4", R.id.tglDevice4);
	}
	
	private void initLabelMap() {
		labelMap = new HashMap<String, Integer>();
		labelMap.put("1", R.id.lblDevice1);
		labelMap.put("2", R.id.lblDevice2);
		labelMap.put("3", R.id.lblDevice3);
		labelMap.put("4", R.id.lblDevice4);
	}

	private void populateRelaysFromJson(String json) {
		Gson gson = new Gson();
        LinkedTreeMap<String, Object> result = gson.fromJson(json, LinkedTreeMap.class);
        List<LinkedTreeMap<String, Object>> items = (List<LinkedTreeMap<String, Object>>) result.get("objects");
        
        this.relays = new ArrayList<Relay>();
        
        for (LinkedTreeMap<String, Object> item : items) { 
        	Relay relay = new Relay();
        	relay.setId((int)Float.parseFloat(item.get("id").toString()));        	
        	relay.setChannel((int)Float.parseFloat(item.get("channel").toString()));
        	relay.setDevice(item.get("device").toString());
        	relay.setActive(Boolean.parseBoolean(item.get("active").toString()));
        	this.relays.add(relay);        	
		}
	}
	
	private int exitCodeFromJson(String json) {
        Gson gson = new Gson();
        LinkedTreeMap<String, Object> result = gson.fromJson(json, LinkedTreeMap.class);

		return (int)Float.parseFloat(result.get("result").toString()); 		
	}
	
}
