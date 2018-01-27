using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour {

	private Rigidbody rb;
	public float speed;
	private float seconds;
	private float minutes;
	private int count;
	public Text countText;
	public Text winText;
	public Text timerText;
	public float jumpHeight;
	private float onGround;

	void Start () {
		rb = GetComponent<Rigidbody> ();
		count = 0;
		SetCountText ();
		winText.text = "";
		timerText.text = "";

		SetTimerText ();
	}

	void Update () {
		if (count < 12) {
			SetTimerText ();
		}
	}

	void FixedUpdate () {
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");
		float jump = Input.GetAxis ("Jump");
		if (transform.position.y == 0.5) {
			onGround = 1;
		} 
		else {
			onGround = 0;
		}


		Vector3 movement = new Vector3 (moveHorizontal, jump * onGround * jumpHeight, moveVertical);

		rb.AddForce (movement * speed);
	}

	void OnTriggerEnter(Collider other) {
		if (other.gameObject.CompareTag ("Pick Up")) {
			other.gameObject.SetActive (false);
			count += 1;
			SetCountText ();
		}
	}

	void SetCountText () {
		countText.text = "Count: " + count.ToString ();
		if (count >= 12) {
			winText.text = "You Win!";
		}
	}

	void SetTimerText () {
		seconds += Time.deltaTime;
		if (seconds > 59.5f) {
			seconds -= 59.5f;
			minutes += 1;
		}
		timerText.text = "Time: " + minutes.ToString ("00") + ":" + seconds.ToString ("00");
	}
}

