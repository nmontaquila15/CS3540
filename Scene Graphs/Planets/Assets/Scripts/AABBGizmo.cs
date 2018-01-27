using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AABBGizmo : MonoBehaviour 
{
	private Bounds bound;

	void Update()
	{
		GetBounds (transform);
	}

	void GetBounds(Transform child)
	{
		bound.Encapsulate (child.GetComponent<Renderer> ().bounds);
		if (child.childCount > 0) {
			for (int i = 0; i < child.childCount; i++) {
				GetBounds (child.GetChild (i));
			}
		}
	}

	void OnDrawGizmos()
	{
		Gizmos.color = Color.white;
		Gizmos.DrawWireCube (transform.position, bound.size);
		Gizmos.DrawWireCube (transform.GetChild(0).position, transform.GetChild(0).GetComponent<Renderer> ().bounds.size);
	}
}
