using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {

	public GameObject player;
	private Vector3 offset;

	void Start () {
		offset = transform.position - player.transform.position; //initialize camera offset from player
	}

	void LateUpdate () {
		transform.position = player.transform.position + offset; //update camera position once per frame after all other items have been processed
	}
}
