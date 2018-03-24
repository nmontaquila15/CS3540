using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class Navigation : MonoBehaviour {

	NavMeshAgent agent;

	void Start() {
		agent = GetComponent<NavMeshAgent>();
	}

	void Update() {
		if (Input.GetMouseButtonDown(0)) {
			RaycastHit hit;

			if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out hit, 100)) {
				if (hit.collider.CompareTag("Terrain"))
					agent.destination = hit.point;
			}
		}
	}
}
