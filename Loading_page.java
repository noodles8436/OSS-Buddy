package com.djy.budy;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

public class Loading_page extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading_page);
        Handler handler = new Handler();
        handler.postDelayed(new Runnable(){
            public void run(){
               // Intent intent = new Intent(getBaseContext(), User_select.class);
               // startActivity(intent);
                 startActivity(new Intent(Loading_page.this,LoginActivity.class));
                finish();
            }
        }, 3000);


    }
}