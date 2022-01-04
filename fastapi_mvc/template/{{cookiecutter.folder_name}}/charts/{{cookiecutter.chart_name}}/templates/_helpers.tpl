{% raw %}{{/*
Expand the name of the chart.
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.labels" -}}
helm.sh/chart: {{ include "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.chart" . }}
{{ include "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.selectorLabels" -}}
app.kubernetes.io/name: {{ include "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "{% endraw %}{{cookiecutter.chart_name}}{% raw %}.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
{% endraw %}