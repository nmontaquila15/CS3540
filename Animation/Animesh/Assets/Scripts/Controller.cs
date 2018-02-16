using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Controller : MonoBehaviour { 
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown (KeyCode.Space)) 
		{
			gameObject.GetComponent<Animator>().SetTrigger ("Switch");
		}

		//was having error where hitting enter while in third state would make it jump back to third state after switching to first state after hitting space
		if (Input.GetKeyDown (KeyCode.Return) && gameObject.GetComponent<Animator> ().GetCurrentAnimatorStateInfo (0).IsName ("Third Animation") == false) 
		{
			gameObject.GetComponent<Animator>().SetTrigger ("Special");
		}
	}
}
