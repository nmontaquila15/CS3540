using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour {

	private Rigidbody2D rb2d;
	private int count;

	public float speed;
	public Text countText;
	public Text winText;

	void Start() {
		rb2d = GetComponent<Rigidbody2D> ();
		count = 0;
		SetCountText ();
		winText.text = "";
	}
		
	void FixedUpdate() {
		float moveHorizontal = Input.GetAxis ("Horizontal");
		float moveVertical = Input.GetAxis ("Vertical");
		Vector2 movement = new Vector2 (moveHorizontal, moveVertical);
		rb2d.AddForce (movement * speed);
	}

	void OnTriggerEnter2D(Collider2D other) {
		if (other.gameObject.CompareTag ("PickUp")) {
			other.gameObject.SetActive (false);
			count++;
			SetCountText ();
		}

		else if (other.gameObject.CompareTag ("Platinum PickUp")) {
			other.gameObject.SetActive (false);
			count += 2;
			SetCountText ();
		}
	}

	void SetCountText() {
		countText.text = "Count: " + count.ToString ();
		if (count >= 12)
			winText.text = "You win!";
		if (count == 20)
			winText.text = "You REALLY win!";
	}
}
