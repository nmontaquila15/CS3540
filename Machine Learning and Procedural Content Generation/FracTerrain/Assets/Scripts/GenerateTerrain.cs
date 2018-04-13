using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GenerateTerrain : MonoBehaviour {

	public Vector3[] newVertices;
	//public Vector2[] newUV;
	public int[] newTriangles;

	// Use this for initialization
	void Start () {
		MeshFilter mf = GetComponent<MeshFilter> ();
		newTriangles = mf.mesh.triangles;
		newVertices = mf.mesh.vertices;

		newVertices = new Vector3[] {new Vector3(-9,0,9),new Vector3(9,0,9),new Vector3(9,0,-9),new Vector3(-9,0,-9)};
		//newUV = new Vector2[] {new Vector2(0,256),new Vector2(256,256),new Vector2(256,0),new Vector2(0,0)};
		newTriangles = new int[] {0,1,2,0,2,3};

		mf.mesh.vertices = newVertices;
		mf.mesh.triangles = newTriangles;
		//mf.mesh.uv = newUV;
		mf.mesh.RecalculateBounds();
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
