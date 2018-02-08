from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property

from entities.models import Person, Institution


class RepoObject(models.Model):
    has_title = models.CharField(
        max_length=250, blank=True, verbose_name="acdh:hasTitle",
        help_text="Title or name of Collection."
    )
    description = models.TextField(
        blank=True, null=True, verbose_name="acdh:hasDescription",
        help_text="A verbose description of certain aspects of an entity. \
        This is the most generic property, use more specific sub-properties where applicable."
    )
    acdh_id = models.CharField(
        max_length=250, blank=True, verbose_name="acdh:hasIdentifier",
        help_text="Unique identifier given by ACDH and used in ACDH systems,\
        as well as identifiers with a stable URL or URI assigned by other parties"
    )
    checked = models.BooleanField(
        blank=True, default=False, verbose_name="Checked",
        help_text="Set to True if the Object passed your internal quality control"
    )
    has_license = models.CharField(
        max_length=250, blank=True, verbose_name="acdh:hasLicense",
        help_text="Denotes the license attached to an object."
    )

    class Meta:
        abstract = True


class Collection(RepoObject):
    part_of = models.ForeignKey(
        'Collection', blank=True, null=True, verbose_name="acdh:isPartOf",
        help_text="Indicates A is a part of aggregate B, \
        e. g. elements of a series, items of a collection.", related_name="has_part",
        on_delete=models.CASCADE
    )
    has_contributor = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasContributor",
        help_text="Agent (person, group, organisation) (B) who was actively involved in \
        creating/curating/editing a Resource, a Collection or in a Project (A).",
        related_name="contributes_to_collection"
    )
    has_creator = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasCreator",
        help_text="Person (B) responsible for creation of resource (A).\
        Will be included in the citation.",
        related_name="created_collection"
    )

    def __str__(self):
        return "{}".format(self.has_title)

    def get_absolute_url(self):
        return reverse('arche:collection_detail', kwargs={'pk': self.id})

    @classmethod
    def get_createview_url(self):
        return reverse('arche:collection_create')

    @classmethod
    def get_listview_url(self):
        return reverse('arche:browse_collections')

    @classmethod
    def get_arche_dump(self):
        return reverse('arche:rdf_collections')

    def get_next(self):
        next = Collection.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Collection.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False


class Resource(RepoObject):
    """
    Mimiks acdh:Resource class:
    Basic entity in the schema containing actual data / content payload; \
    comparable (and mostly equivalent) to files in a file system.
    """

    has_creator = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasContributor",
        help_text="Agent (person, group, organisation) (B) who was actively involved in \
        creating/curating/editing a Resource, a Collection or in a Project (A).",
        related_name="created_resource"
    )
    has_contributor = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasContributor",
        help_text="Agent (person, group, organisation) (B) who was actively involved in \
        creating/curating/editing a Resource, a Collection or in a Project (A).",
        related_name="contributes_to_resource"
    )
    has_filetype = models.CharField(
        max_length=250, blank=True, verbose_name="acdh:hasFormat",
        help_text="Format of a resource (A). Indicated as MIME type."
    )

    file_size = models.IntegerField(
        blank=True, null=True, verbose_name="acdh:hasBinarySize",
        help_text="Indicates size in bytes of a Resource or Collection"
    )
    part_of = models.ForeignKey(
        'Collection', blank=True, null=True, verbose_name="acdh:isPartOf",
        help_text="Indicates A is a part of aggregate B, \
        e. g. elements of a series, items of a collection.", related_name="has_part_resource",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{}".format(self.has_title)

    def get_absolute_url(self):
        return reverse('arche:resource_detail', kwargs={'pk': self.id})

    @classmethod
    def get_createview_url(self):
        return reverse('arche:resource_create')

    @classmethod
    def get_listview_url(self):
        return reverse('arche:browse_resources')

    def inherit_properties(self):
        """ fetches (some) properties of the part_of collection\
        and saves it to the current object"""

        license = self.part_of.has_license
        if license:
            self.has_license = license
            self.save()
        else:
            license = None
        creators = self.part_of.has_creator.all()
        for x in creators:
            self.has_creator.add(x)
        contributors = self.part_of.has_contributor.all()
        for x in contributors:
            self.has_contributor.add(x)
        return [creators, contributors, license]
    # @classmethod
    # def get_arche_dump(self):
    #     return reverse('arche:rdf_resources')

    def get_next(self):
        next = Resource.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Resource.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def label(self):
        if self.acdh_id:
            return self.acdh_id
        else:
            return "{}/{}".format(self.part_of.has_title, self.has_title)


class Project(RepoObject):
    has_principal = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasPrincipalInvestigator",
        help_text="Person officially designated as head of project team or subproject \
        team instrumental in the work necessary to development of the resource.",
        related_name="is_principal"
    )
    has_contributor = models.ManyToManyField(
        Person, blank=True, verbose_name="acdh:hasContributor",
        help_text="Agent (person, group, organisation) (B) who was actively involved in \
        creating/curating/editing a Resource, a Collection or in a Project (A).",
        related_name="contributes_to_project"
    )
    has_start_date = models.DateField(
        blank=True, null=True, verbose_name="acdh:hasStartDate",
        help_text="Indicates the start date of a Project."
    )
    has_end_date = models.DateField(
        blank=True, null=True, verbose_name="acdh:hasEndtDate",
        help_text="Indicates the end date of a Project."
    )
    has_funder = models.ManyToManyField(
        Institution, blank=True, verbose_name="acdh:hasFunder",
        help_text="Organisation (B) which provided funding for the project (A).",
        related_name="is_funding"
    )
    related_collection = models.ManyToManyField(
        Collection, blank=True, verbose_name="acdh:hasRelatedCollection",
        help_text="Indication of a project (B) associated with this resource or collection (A).",
        related_name="has_related_project"
    )

    def __str__(self):
        return "{}".format(self.has_title)

        def get_absolute_url(self):
            return reverse('arche:project_detail', kwargs={'pk': self.id})

    def get_absolute_url(self):
        return reverse('arche:project_detail', kwargs={'pk': self.id})

    @classmethod
    def get_createview_url(self):
        return reverse('arche:project_create')

    @classmethod
    def get_listview_url(self):
        return reverse('arche:browse_projects')

    @classmethod
    def get_arche_dump(self):
        return reverse('arche:rdf_projects')

    def get_next(self):
        next = Project.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Project.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False
