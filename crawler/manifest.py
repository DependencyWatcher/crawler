import os
import json

def subst_vars(e, vars):
	""" Substitutes variables inside given object """
	if isinstance(e, dict):
		for k, v in e.iteritems():
			e[k] = subst_vars(v, vars)
	elif isinstance(e, list):
		return [subst_vars(v, vars) for v in e]
	else:
		for k, v in vars.iteritems():
			e = e.replace("${%s}" % k, v)
	return e

class ManifestLoader():
	""" Abstract dependency manifest loader """

	def read_manifest(self, name):
		""" Reads manifest """
		raise NotImplementedError

	def read_template(self, name):
		""" Reads manifest template """
		raise NotImplementedError

	def read_all_manifests(self, name):
		""" Returns generator allowing to iterate on all manifests """
		raise NotImplementedError

	def merge(self, template, manifest):
		""" Merges values from manifest into template """
		for k, v in manifest.iteritems():
			if isinstance(v, dict):
				if not k in template:
					template[k] = {}
				self.merge(template[k], v)
			else:
				template[k] = v

	def postload(self, manifest):
		""" This method resolves extended template, and substitutes needed variables into loaded manifest """
		vars = {"NAME": manifest["name"]}
		try:
			extends = manifest["extends"]
			try:
				for v in extends["vars"]:
					vars[v["name"]] = v["value"]
			except KeyError:
				pass

			template = self.read_template(extends["template"])
			del manifest["extends"]

			self.merge(template, manifest)
			manifest = template
		except KeyError:
			pass

		manifest = subst_vars(manifest, vars)
		return manifest

	def load(self, name):
		""" Loads manifest """
		manifest = self.read_manifest(name)
		return self.postload(manifest)

	def load_all(self):
		""" Returns generator of all existing manifests """
		for manifest in self.read_all_manifests():
			yield self.postload(manifest)


class FileManifestLoader(ManifestLoader):
	""" Manifest loader that looks for JSON files in file system """
	def __init__(self, parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "manifests")):
		self.parent_dir = parent_dir

	def get_file(self, name, prefix_dir=""):
		return os.path.join(self.parent_dir, prefix_dir, "/".join([i for i in name[0:4]]), "%s.json" % name)

	def read_manifest(self, name):
		with open(self.get_file(name, "_m")) as f:
			return json.load(f)

	def read_template(self, name):
		with open(self.get_file(name, "_t")) as f:
			return json.load(f)

	def read_all_manifests(self):
		for root, dirs, files in os.walk(os.path.join(self.parent_dir, "_m")):
			for name in files:
				if name.endswith(".json"):
					with open(os.path.join(root, name)) as f:
						yield json.load(f)

class DBManifestLoader(ManifestLoader):
	""" Manifest loader that looks for JSON objects in DB """
	pass

