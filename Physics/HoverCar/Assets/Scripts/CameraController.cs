using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour
{
	public GameObject player;

	private Vector3 offset;
	private float height;

	void Start ()
	{
		offset = player.transform.InverseTransformPoint (transform.position);
		height = transform.position.y;
	}

	void LateUpdate ()
	{
		Vector3 desiredPostion = player.transform.TransformPoint (offset);
		desiredPostion.y = height;
		transform.position = desiredPostion;
		transform.LookAt (player.transform);
	}
}
