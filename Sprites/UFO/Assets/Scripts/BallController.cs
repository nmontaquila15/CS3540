using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallController : MonoBehaviour {

	private Rigidbody2D rb2d;

	public float speed;

	// Send ball in randomized direction at start
	void Start () {
		rb2d = GetComponent<Rigidbody2D> ();
		float x = Random.Range (-1.0f, 1.0f);
		float y = Random.Range (-1.0f, 1.0f);
		Vector2 direction = new Vector2 (x, y);
		rb2d.AddForce (direction.normalized * speed);
	}

}
